from ...extension import db

class Appointment(db.Model):
    __tablename__ = 'appointment'

    uid = db.Column(db.Integer, primary_key = True)
    
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    
    date = db.Column(db.Date, nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    status = db.Column(db.String(50), default='pending')

    doctor = db.relationship('User', foreign_keys=[doctor_id])
    member = db.relationship('User', foreign_keys=[member_id])

    def __repr__(self):
        return f'Appointment with name {self.name} and associated doctor {self.doctor}'

    def get_id(self):
        return self.uid