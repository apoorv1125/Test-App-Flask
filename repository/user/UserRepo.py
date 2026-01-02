# from models.User.user_model import User
# from models.User.user_model import UserRole
from models.User.user_model import User
from .UserRepoModel import UserRepoModel
from extension import db

class UserRepo:
    def __init__(self) -> None:
        pass

    def save_user(self, email, role, pwd):
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already registered")

        user = User(email=email, password_hash=pwd, role=role)
        db.session.add(user)
        db.session.commit()

        # if role==UserRole.DOCTOR:
            # doc = Doctor(user_id=user.id)
            # db.session.add(doc)
            # db.session.commit()

    def get_user_auth_details(self, email):
        user = User.query.filter_by(email=email).first()
        # roleId = Doctor.query.filter_by(user_id=user.id).first().id if user.role == UserRole.DOCTOR else user.id
        # if not user or not roleId:
        if not user:
            raise ValueError("ResourceNotFoundException")
        return UserRepoModel(user_id=user.id, email=user.email, role=user.role , pwd=user.password_hash)
