from flask_jwt_extended import create_access_token
from repository.user.UserRepo import UserRepo
from models.User.user_model import UserRole
from utils import hash_password, verify_password

##Service which creates the user in the database.
def register_user(email: str, password: str, role: str = UserRole.MEMBER):
    user_repo = UserRepo()
    user_repo.save_user(email=email, role= role, pwd= hash_password(password))

def authenticate_user(email: str, password: str):
    user_repo = UserRepo()
    user = user_repo.get_user_auth_details(email)
    if not user:
        return None
    if not verify_password(user.pwd, password):
        return None
    additional_claims = {"role": user.role}
    access_token = create_access_token(
        identity=str(user.user_id), additional_claims=additional_claims
    )
    return access_token
