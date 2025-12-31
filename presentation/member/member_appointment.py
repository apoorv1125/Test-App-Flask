#%%
from flask_jwt_extended import jwt_required

from ...repository.appointment.AppointmentModel import AppointmentModel
from ...Exceptions import ActionNotAllowedException, AlreadyExistsException, NoAvailabilityException
from ...services.appointment_service import book_appointment_service, appointment_list_service, delete_appointment_service
from ...services.availability_service import availability_list_service
from ...utils import roles_required

from flask import Blueprint, request, jsonify
from ...schema.appointment.AppointmentSchema import AppointmentSchema

from ...models.User.user_model import UserRole

member_bp = Blueprint("member", __name__)

@member_bp.route("/book_appointment", methods=["POST"])
@jwt_required()
@roles_required(UserRole.MEMBER)
def book_appointment():
    data = request.get_json() or {}
    errors = AppointmentSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    try:
        result = book_appointment_service(
            AppointmentModel(
                date = data.get("date"),
                doctorId = data.get("doctorId"),
                memberId=data.get("memberId"),
                startTime = data.get("startTime"),
                endTime = data.get("endTime")
            )
        )

    except NoAvailabilityException as e:
        return jsonify({"errors": "There is no availability"}), 400
    except AlreadyExistsException as e:
        return jsonify({"errors": "Time Already added"}), 400
    except ActionNotAllowedException as e:
        return jsonify({"errors": "Invalid action"}), 400
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify({"message": "Appointment set"}), 201


@member_bp.route("/available_slots/<int:doctor_id>", methods=["GET"])
@jwt_required()
@roles_required(UserRole.MEMBER)
def available_slots(doctor_id):
    try:
        result = availability_list_service(doctor_id)
        response = []
        for d in result:
            department_info = {
                "id": d.id,
                "doctorId": d.doctorId,
                "doctorName": d.doctorName,
                "date": d.date.isoformat(),
                "startTime": d.startTime.strftime("%H:%M"),
                "endTime": d.endTime.strftime("%H:%M"),
            }
            response.append(department_info)

    except AlreadyExistsException as e:
        return jsonify({"errors": "Time Already added"}), 400
    except ActionNotAllowedException as e:
        return jsonify({"errors": "Invalid action"}), 400
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify({"message":response}), 200


@member_bp.route("/appointments/<int:member_id>", methods=["GET"])
@jwt_required()
@roles_required(UserRole.MEMBER)
def booked_appointments(member_id):
    try:
        result = appointment_list_service(member_id)
        response = []
        for d in result:
            department_info = {
                "id": d.id,
                "doctorId": d.doctorId,
                "doctorName": d.doctorName,
                "date": d.date.isoformat(),
                "startTime": d.startTime.strftime("%H:%M"),
                "endTime": d.endTime.strftime("%H:%M"),
            }
            response.append(department_info)

    except AlreadyExistsException as e:
        return jsonify({"errors": "Time Already added"}), 400
    except ActionNotAllowedException as e:
        return jsonify({"errors": "Invalid action"}), 400
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify({"message":response}), 201


@member_bp.route("/delete_appointment/<int:appointment_id>", methods=["POST"])
@jwt_required()
@roles_required(UserRole.MEMBER)
def delete_department(appointment_id):
    try:
        result = delete_appointment_service(
            appointment_id
        )
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify({"Result": result}), 200
