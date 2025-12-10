from app import db
from flask_login import UserMixin

# class Person(db.Model):
#     __tablename__ = 'people'

#     pid = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     age = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f'Person with name ${self.name} and age ${self.age}'

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'User with name {self.name} and role {self.role} and {self.password}'
    
    def get_id(self):
        return self.uid