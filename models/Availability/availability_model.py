from ...extension import db

class Availability(db.Model):
    __tablename__ = 'availability'

    uid = db.Column(db.Integer, primary_key=True)
    
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    doctor = db.relationship('User', foreign_keys=[doctor_id])

    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'Availability with name {self.doctor} and {self.start_time}-{self.end_time}'

    def get_id(self):
        return self.uid
