from models.Department.department_model import Department
# from app.datalayer.entities.Doctor import Doctor
# from app.datalayer.entities.DoctorAvailability import DoctorAvailability
from Exceptions import (ActionNotAllowedException, AlreadyExistsException)
from .DepartmentModel import DepartmentModel
from extension import db
from sqlalchemy import func

class DepartmentsRepo:
    def __init__(self) -> None:
        pass

    def get_all_departments(self):
        results = Department.query.all()
        return [
            DepartmentModel(doctorId=u.doctor_id, name=u.name, doctorName=u.doctor.email, id = u.uid)
            for u in results
        ]

    def save_department(self, dataModel: DepartmentModel):
        try:
            dbModel = Department()
            dbModel.name = dataModel.name
            dbModel.doctor_id = dataModel.doctorId if dataModel.doctorId != "" else None

            existing_department = Department.query.filter(
                func.lower(Department.name) == dbModel.name.lower()
            ).first()

            if existing_department:
                raise AlreadyExistsException()

            db.session.add(dbModel)
            db.session.commit()
        except:
            db.session.rollback()
            raise ActionNotAllowedException()
        return dataModel


    def update_department(self, department_id, dataModel: DepartmentModel):
        try:
            department = Department.query.get_or_404(department_id)

            existing_department = Department.query.filter(
                func.lower(Department.name) == dataModel.name.lower()
            ).first()

            if existing_department:
                raise AlreadyExistsException()

            department.name = dataModel.name
            department.doctor_id = dataModel.doctorId

            db.session.commit()
        except:
            db.session.rollback()
            raise ActionNotAllowedException()
        return dataModel

    def delete_department(self, department_id):
        try:
            department_to_delete = Department.query.get_or_404(department_id)
            db.session.delete(department_to_delete)
            db.session.commit()
        except:
            db.session.rollback()
            raise ActionNotAllowedException()
        return True
