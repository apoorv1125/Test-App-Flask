from models.Availability.availability_model import Availability
from Exceptions import (ActionNotAllowedException, AlreadyExistsException)
from .AvailabilityModel import AvailabilityModel
from extension import db
from datetime import datetime

class AvailabilityRepo:
    def __init__(self) -> None:
        pass

    def get_all_availability(self):
        results = Availability.query.all()
        return [
            AvailabilityModel(doctorId=u.doctor_id, doctorName=u.doctor.email, date=u.date, startTime=u.start_time, endTime=u.end_time, id = u.uid)
            for u in results
        ]

    def get_doctor_availability(self, doctor_id):
        results = Availability.query.filter_by(doctor_id=doctor_id).all()
        return [
            AvailabilityModel(doctorId=u.doctor_id, doctorName=u.doctor.email, date=u.date, startTime=u.start_time, endTime=u.end_time, id = u.uid)
            for u in results
        ]

    def save_availability(self, dataModel: AvailabilityModel):
        try:
            dbModel = Availability()

            dbModel.doctor_id = dataModel.doctorId if dataModel.doctorId != "" else None

            date_obj = datetime.strptime(dataModel.date, "%Y-%m-%d").date()
            start_time_obj = datetime.strptime(dataModel.startTime, "%H:%M").time()
            end_time_obj = datetime.strptime(dataModel.endTime, "%H:%M").time()

            dbModel.date = date_obj
            dbModel.start_time = start_time_obj
            dbModel.end_time = end_time_obj

            existing_slots = Availability.query.filter_by(
                doctor_id=dataModel.doctorId,
                date=date_obj
            ).all()

            for slot in existing_slots:
                if start_time_obj < slot.end_time and end_time_obj > slot.start_time:
                    # f"Conflict: Existing slot {slot.start_time}-{slot.end_time}", 400
                    raise AlreadyExistsException()

            db.session.add(dbModel)
            db.session.commit()
        except:
            db.session.rollback()
            raise ActionNotAllowedException()
        return dataModel

    def delete_availablity(self, availability_id):
        try:
            item_to_delete = Availability.query.get_or_404(availability_id)
            db.session.delete(item_to_delete)
            db.session.commit()
        except:
            db.session.rollback()
            raise ActionNotAllowedException()
        return True

