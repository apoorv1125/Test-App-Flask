from repository.availability.AvailabilityRepo import AvailabilityRepo

def save_availability_service(dataModel):
    dataModel = AvailabilityRepo().save_availability(dataModel)
    return dataModel

def delete_availability_service(availability_id):
    dataModel = AvailabilityRepo().delete_availablity(availability_id)
    return dataModel

def availability_list_service(doctor_id):
    return AvailabilityRepo().get_doctor_availability(doctor_id)
