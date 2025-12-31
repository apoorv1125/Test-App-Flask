from ..repository.appointment.AppointmentRepo import AppointmentRepo

def book_appointment_service(dataModel):
    dataModel = AppointmentRepo().book_appointment(dataModel)
    return dataModel

def delete_appointment_service(appointment_id):
    dataModel = AppointmentRepo().delete_appointment(appointment_id)
    return dataModel

def appointment_list_service(member_id):
    return AppointmentRepo().get_member_appointments(member_id)
