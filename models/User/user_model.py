from ...extension import db
from flask_login import UserMixin
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    MEMBER = "member"

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(200), nullable=False)
    password_hash: str = db.Column(db.String(200), nullable=False)
    role: str = db.Column(db.String(20), nullable=False, default=UserRole.MEMBER)

    def __repr__(self):
        return f'User with name {self.email} and role {self.role} and pass {self.password_hash}'

    def get_id(self):
        return self.id