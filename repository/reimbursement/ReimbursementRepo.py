from ...models.Reimbursement.reimbursement_model import Reimbursement
from ...Exceptions import (ActionNotAllowedException, AlreadyExistsException)
from .ReimbursementModel import ReimbursementModel
from ...extension import db

class ReimbursementRepo:
    def __init__(self) -> None:
        pass

    def get_all_reimbursements(self):
        results = Reimbursement.query.all()
        return [
            ReimbursementModel(
                doctorId=u.doctor_id,
                doctorName=u.doctor.email,
                memberId=u.member_id,
                memberName=u.member.email,
                departmentId=u.department_id,
                departmentName=u.department.name,
                status=u.status,
                amount=u.amount,
                id = u.uid
            )
            for u in results
        ]

    def get_reimbursements(self, claim_id):
        results = Reimbursement.query.filter_by(uid = claim_id).first()
        return [
            ReimbursementModel(
                doctorId=u.doctor_id,
                doctorName=u.doctor.email,
                memberId=u.member_id,
                memberName=u.member.email,
                departmentId=u.department_id,
                departmentName=u.department.name,
                status=u.status,
                amount=u.amount,
                id = u.uid
            )
            for u in results
        ]

    def create_claim(self, dataModel: ReimbursementModel):
        try:
            dbModel = Reimbursement(
                doctor_id=dataModel.doctorId,
                member_id=dataModel.memberId,
                department_id=dataModel.departmentId,
                amount=dataModel.amount,
                status=dataModel.status,
            )

            db.session.add(dbModel)
            db.session.commit()
        except:
            db.session.rollback()
            raise ActionNotAllowedException()
        return dataModel


    def update_claim_status(self, claim_id, status):

        item_to_update = Reimbursement.query.get_or_404(claim_id)
        item_to_update.status = status
        model = ReimbursementModel(
            id = item_to_update.uid,
            doctorId = item_to_update.doctor_id,
            doctorName = item_to_update.doctor.email,
            departmentId = item_to_update.department_id,
            departmentName = item_to_update.department.name,
            memberId = item_to_update.member_id,
            memberName = item_to_update.member.email,
            status = item_to_update.status,
            amount = item_to_update.amount,
        )
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise ActionNotAllowedException()
        return model

    def delete_claim(self, claim_id):
        try:
            item_to_delete = Reimbursement.query.get_or_404(claim_id)
            db.session.delete(item_to_delete)
            db.session.commit()
        except:
            db.session.rollback()
            raise ActionNotAllowedException()
        return True

