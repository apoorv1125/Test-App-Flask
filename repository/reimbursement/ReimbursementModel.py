from dataclasses import dataclass

from marshmallow.fields import Date


@dataclass
class ReimbursementModel:
    id: int | None = None
    doctorId: int | None = None
    doctorName: str | None = None
    departmentId: str | None = None
    departmentName: str | None = None
    memberId: str | None = None
    memberName: str | None = None
    status: str | None = None
    amount: int | None = None
