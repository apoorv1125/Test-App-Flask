from dataclasses import dataclass, field

@dataclass
class UserRepoModel:
    user_id: int
    email: str
    role: str
    pwd: str = field(default="",repr=False)