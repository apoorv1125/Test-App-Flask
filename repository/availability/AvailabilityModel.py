from dataclasses import dataclass

from marshmallow.fields import Date


@dataclass
class AvailabilityModel:
    id: int | None = None
    doctorId: int | None = None
    doctorName: str | None = None
    date: str | None = None
    startTime: str | None = None
    endTime: str | None = None
