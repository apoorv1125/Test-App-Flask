from dataclasses import dataclass

@dataclass
class DepartmentModel:
    name: str | None
    id: str | None = None
    doctorId: int | None = None
    doctorName: int | None = None
