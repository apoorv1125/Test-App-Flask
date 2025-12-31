from flask_jwt_extended import jwt_required, get_jwt_identity

from ..Exceptions import ActionNotAllowedException, AlreadyExistsException
from ..services.admin_services import departments_list_service

from flask import Blueprint, jsonify
from ..models.User.user_model import UserRole

from ..utils import roles_required

department_bp = Blueprint("department", __name__)

@department_bp.route("/list", methods=["GET"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def get_department():
    try:
        result = departments_list_service()
        response = []
        for d in result:
            department_info = {
                "id": d.id,
                "name": d.name,
                "doctorId": d.doctorId,
                "doctorName": d.doctorName
            }
            response.append(department_info)

    except ActionNotAllowedException as e:
        return jsonify({"errors": "Invalid action"}), 400
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify(response), 200