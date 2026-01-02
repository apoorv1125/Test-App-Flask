from flask_jwt_extended import jwt_required

from repository.availability.AvailabilityModel import AvailabilityModel
from Exceptions import ActionNotAllowedException, AlreadyExistsException
from services.availability_service import save_availability_service, delete_availability_service
from utils import roles_required

from flask import Blueprint, request, jsonify
from schema.availability.AvailabilitySchema import AvailabilitySchema

from models.User.user_model import UserRole

doctor_bp = Blueprint("doctor", __name__)

@doctor_bp.route("/create_availability", methods=["POST"])
@jwt_required()
@roles_required(UserRole.DOCTOR)
def save_availability():
    data = request.get_json() or {}
    errors = AvailabilitySchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    try:
        result = save_availability_service(
            AvailabilityModel(
                date = data.get("date"),
                doctorId = data.get("doctorId"),
                startTime = data.get("startTime"),
                endTime = data.get("endTime")
            )
        )
    except AlreadyExistsException as e:
        return jsonify({"errors": "Time Already added"}), 400
    except ActionNotAllowedException as e:
        return jsonify({"errors": "Invalid action"}), 400
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify({"message": "Availability set"}), 201

@doctor_bp.route("/delete_availability/<int:availability_id>", methods=["POST"])
@jwt_required()
@roles_required(UserRole.DOCTOR)
def delete_availability(availability_id):
    try:
        result = delete_availability_service(
            availability_id
        )
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify({"Result": result}), 200
