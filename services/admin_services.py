from ..repository.department.DepartmentRepo import DepartmentsRepo
from ..repository.availability.AvailabilityRepo import AvailabilityRepo
from ..repository.appointment.AppointmentRepo import AppointmentRepo
from ..repository.reimbursement.ReimbursementRepo import ReimbursementRepo

from ..Exceptions import (ResourceNotFoundException)

# Department
def create_department_service(dataModel):
    if not dataModel.name:
        raise ResourceNotFoundException()
    dataModel = DepartmentsRepo().save_department(dataModel)
    return dataModel

def update_department_service(department_id, dataModel):
    if not dataModel.name:
        raise ResourceNotFoundException()
    dataModel = DepartmentsRepo().update_department(department_id, dataModel)
    return dataModel

def delete_department_service(department_id):
    return DepartmentsRepo().delete_department(department_id)

def departments_list_service():
    return DepartmentsRepo().get_all_departments()

# Availability
def availability_all_list_service():
    return AvailabilityRepo().get_all_availability()

# Appointment
def appointment_all_list_service():
    return AppointmentRepo().get_all_appointments()
