from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify

from ...Exceptions import ActionNotAllowedException, AlreadyExistsException
from ...services.admin_services import create_department_service, update_department_service, delete_department_service, departments_list_service, appointment_all_list_service, availability_all_list_service
from ...repository.department.DepartmentModel import DepartmentModel
from ...utils import roles_required
from ...schema.department.departmentSchema import DepartmentSchema
from ...models.User.user_model import UserRole

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def admin_dashboard():
    try:
        departments = departments_list_service()
        response_departments = []
        for d in departments:
            department_info = {
                "id": d.id,
                "name": d.name,
                "doctorId": d.doctorId,
                "doctorName": d.doctorName
            }
            response_departments.append(department_info)

        availability = availability_all_list_service()
        response_availability = []
        for d in availability:
            department_info = {
                "id": d.id,
                "doctorId": d.doctorId,
                "doctorName": d.doctorName,
                "date": d.date.isoformat(),
                "startTime": d.startTime.strftime("%H:%M"),
                "endTime": d.endTime.strftime("%H:%M"),
            }
            response_availability.append(department_info)

        appointments = appointment_all_list_service()
        response_appointments = []
        for d in appointments:
            department_info = {
                "id": d.id,
                "doctorId": d.doctorId,
                "doctorName": d.doctorName,
                "memberId": d.memberId,
                "memberName": d.memberName,
                "date": d.date.isoformat(),
                "startTime": d.startTime.strftime("%H:%M"),
                "endTime": d.endTime.strftime("%H:%M"),
            }
            response_appointments.append(department_info)

    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify({
            "departments": response_departments,
            "appointments": response_appointments,
            "availability": response_availability
        }), 200

@admin_bp.route("/create_department", methods=["POST"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def create_department():
    data = request.get_json() or {}
    errors = DepartmentSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    try:
        result = create_department_service(
            DepartmentModel(name = data.get("name"),doctorId= data.get("doctorId"))
        )
    except AlreadyExistsException as e:
        return jsonify({"errors": "Name Already exists"}), 400
    except ActionNotAllowedException as e:
        return jsonify({"errors": "Invalid action"}), 400
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify(DepartmentSchema().dump(result)), 201

@admin_bp.route("/update_department/<int:department_id>", methods=["POST"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def update_department(department_id):
    data = request.get_json() or {}
    errors = DepartmentSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    try:
        result = update_department_service(
            department_id,
            DepartmentModel(name = data.get("name"),id = department_id, doctorId= data.get("doctorId"))
        )
    except AlreadyExistsException as e:
        return jsonify({"errors": "Name Already exists"}), 400
    except ActionNotAllowedException as e:
        return jsonify({"errors": "Invalid action"}), 400
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify(DepartmentSchema().dump(result)), 200

@admin_bp.route("/delete_department/<int:department_id>", methods=["POST"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def delete_department(department_id):
    try:
        result = delete_department_service(
            department_id
        )
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify({"Result": result}), 200