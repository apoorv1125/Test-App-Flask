from models.Appointment.appointment_model import Appointment
from models.Availability.availability_model import Availability

from Exceptions import (NoAvailabilityException, AlreadyExistsException, ActionNotAllowedException)
from .AppointmentModel import AppointmentModel
from extension import db
from datetime import datetime

class AppointmentRepo:
    def __init__(self) -> None:
        pass

    def get_all_appointments(self):
        results = Appointment.query.all()
        return [
            AppointmentModel(doctorId=u.doctor_id, doctorName=u.doctor.email, memberId=u.member_id, memberName=u.member.email,
                             date=u.date, startTime=u.start_time, endTime=u.end_time, id = u.uid)
            for u in results
        ]

    def get_member_appointments(self, member_id):
        results = Appointment.query.filter_by(member_id=member_id).all()
        return [
            AppointmentModel(doctorId=u.doctor_id, doctorName=u.doctor.email, memberId=u.member_id, memberName=u.member.email,
                             date=u.date, startTime=u.start_time, endTime=u.end_time, id = u.uid)
            for u in results
        ]

    def book_appointment(self, dataModel: AppointmentModel):
        try:
            date = dataModel.date
            doctor_id = dataModel.doctorId
            member_id = dataModel.memberId
            start_time = dataModel.startTime
            end_time = dataModel.endTime

            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            start_time_obj = datetime.strptime(start_time, "%H:%M").time()
            end_time_obj = datetime.strptime(end_time, "%H:%M").time()

            existing_slots = Appointment.query.filter_by(
                doctor_id=doctor_id,
                date=date_obj
            ).all()

            for slot in existing_slots:
                if start_time_obj < slot.end_time and end_time_obj > slot.start_time:
                    # return f"Conflict: Existing appointment in this slot {slot.start_time}-{slot.end_time}", 400
                    raise AlreadyExistsException()

            existing_availability = Availability.query.filter_by(
                doctor_id=doctor_id,
                date=date_obj
            ).all()

            if not existing_availability:
                # return "Doctor has no availability on this date", 400
                raise NoAvailabilityException()

            fits_in_availability = False
            for avail in existing_availability:
                if start_time_obj >= avail.start_time and end_time_obj <= avail.end_time:
                    fits_in_availability = True
                    break

            if not fits_in_availability:
                # return f"Appointment time {start_time_obj}-{end_time_obj} is outside availability availability", 400
                raise NoAvailabilityException()

            appointment = Appointment(
                date=date_obj,
                start_time=start_time_obj,
                end_time=end_time_obj,
                doctor_id=doctor_id if doctor_id != "" else None,
                member_id=member_id if member_id != "" else None
            )

            db.session.add(appointment)
            db.session.commit()
        except:
            db.session.rollback()
            raise ActionNotAllowedException()
        return dataModel

    def delete_appointment(self, appointment_id):
        try:
            item_to_delete = Appointment.query.get_or_404(appointment_id)
            db.session.delete(item_to_delete)
            db.session.commit()
        except:
            db.session.rollback()
            raise ActionNotAllowedException()
        return True
