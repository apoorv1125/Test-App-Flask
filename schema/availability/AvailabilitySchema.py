from marshmallow import Schema, fields

class AvailabilitySchema(Schema):
    id = fields.Int(dump_only=True)
    doctorId = fields.Int(required=True)
    date = fields.Date(required=True)
    startTime = fields.Time(required=True)
    endTime = fields.Time(required=True)