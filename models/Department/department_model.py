from extension import db

class Department(db.Model):
    __tablename__ = 'department'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    doctor = db.relationship('User', backref='departments')
    
    def __repr__(self):
        return f'Department with name {self.name} and associated doctor {self.doctor}'

    def get_id(self):
        return self.uid
