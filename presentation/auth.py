from flask import Blueprint, request, jsonify

from schema.user.UserSchema import RegisterSchema
from schema.user.UserSchema import LoginSchema
from services.auth_services import register_user, authenticate_user
from models.User.user_model import UserRole

# Creates the blueprint for all the endpoint related to the user authentication
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    errors = RegisterSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    email = data["email"]
    password = data["password"]
    role = data.get("role", UserRole.MEMBER)
    try:
        user = register_user(email, password, role)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    return jsonify({"success": True}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    errors = LoginSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    result = authenticate_user(data["email"], data["password"])
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify({"access_token": result}), 200
