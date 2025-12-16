from app import db
from flask_login import UserMixin
from sqlalchemy import Enum
import enum

# class Person(db.Model):
#     __tablename__ = 'people'

#     pid = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     age = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f'Person with name ${self.name} and age ${self.age}'

class UserRole(enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    MEMBER = "member"

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(
        Enum(UserRole, name="user_role_enum"),
        nullable=False
    )

    def __repr__(self):
        return f'User with name {self.name} and role {self.role}'
    
    def get_id(self):
        return self.uid

class Department(db.Model):
    __tablename__ = 'department'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    doctor_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    doctor = db.relationship('User', backref='departments')
    
    def __repr__(self):
        return f'Department with name {self.name} and associated doctor {self.doctor}'

    def get_id(self):
        return self.uid

class Availability(db.Model):
    __tablename__ = 'availability'

    uid = db.Column(db.Integer, primary_key=True)
    
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    doctor = db.relationship('User', foreign_keys=[doctor_id])

    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'Availability with name {self.doctor} and {self.start_time}-{self.end_time}'

    def get_id(self):
        return self.uid
    
class Appointment(db.Model):
    __tablename__ = 'appointment'

    uid = db.Column(db.Integer, primary_key=True)
    
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    member_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default='pending')

    doctor = db.relationship('User', foreign_keys=[doctor_id])
    member = db.relationship('User', foreign_keys=[member_id])

    def __repr__(self):
        return f'Appointment with name {self.name} and associated doctor {self.doctor}'

    def get_id(self):
        return self.uid