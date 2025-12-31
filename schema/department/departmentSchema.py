from marshmallow import Schema, fields

class DepartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    doctorId = fields.Int(required=True)