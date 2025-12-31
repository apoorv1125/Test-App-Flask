from marshmallow import Schema, fields, validate

class ReimbursementSchema(Schema):
    id = fields.Int(dump_only=True)
    doctorId = fields.Int(required=True)
    memberId = fields.Int(load_only=True)
    departmentId = fields.Int(load_only=True)
    amount = fields.Int(load_only=True)
    status = fields.String(
        required=True, validate=validate.OneOf(["pending", "approved", "rejected"])
    )


class UpdateClaimSchema(Schema):
    id = fields.Int(required=True)
    status = fields.String(
        required=True, validate=validate.OneOf(["pending", "approved", "rejected"])
    )
