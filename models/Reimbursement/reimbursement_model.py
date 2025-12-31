from ...extension import db
import enum

class ClaimStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Reimbursement(db.Model):
    __tablename__ = 'reimbursement'

    uid = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.uid'), nullable=False)

    amount = db.Column(db.Integer, nullable=False)

    status: str = db.Column(db.String(20), nullable=False, default=ClaimStatus.PENDING)

    doctor = db.relationship('User', foreign_keys=[doctor_id])
    member = db.relationship('User', foreign_keys=[member_id])
    department = db.relationship('Department', foreign_keys=[department_id])