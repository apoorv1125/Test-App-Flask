from flask_jwt_extended import jwt_required

from schema.reimbursement.ReimbursementSchema import UpdateClaimSchema
from repository.reimbursement.ReimbursementModel import ReimbursementModel
from Exceptions import ActionNotAllowedException, AlreadyExistsException, NoAvailabilityException
from services.reimbursement_serivce import create_claim, delete_claim, individual_reimbursement_service, reimbursement_all_list_service, update_claim_status
from utils import roles_required

from flask import Blueprint, request, jsonify
from schema.reimbursement.ReimbursementSchema import ReimbursementSchema

from models.User.user_model import UserRole

reimbursement_bp = Blueprint("reimbursement", __name__)

@reimbursement_bp.route("/create_reimbursement", methods=["POST"])
@jwt_required()
@roles_required(UserRole.MEMBER)
def create_reimbursement():
    data = request.get_json() or {}
    errors = ReimbursementSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    try:
        create_claim(
            ReimbursementModel(
                departmentId = data.get("departmentId"),
                doctorId = data.get("doctorId"),
                memberId = data.get("memberId"),
                status = data.get("status"),
                amount = data.get("amount"),
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
    return jsonify({"message": "Reimbursement created"}), 201

@reimbursement_bp.route("/delete_reimbursement/<int:id>", methods=["POST"])
@jwt_required()
@roles_required(UserRole.MEMBER)
def delete_reimbursement(id):
    try:
        result = delete_claim(id)
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify({"Result": result}), 200

@reimbursement_bp.route("/all_reimbursement", methods=["GET"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def get_all_reimbursement():
    try:
        result = reimbursement_all_list_service()
        response = []
        for d in result:
            department_info = {
                "doctorId" : d.doctorId,
                "doctorName" : d.doctorName,
                "memberId" : d.memberId,
                "memberName" : d.memberName,
                "departmentId" : d.departmentId,
                "departmentName" : d.departmentName,
                "status" : d.status,
                "amount" : d.amount,
                "id" : d.id,
            }
            response.append(department_info)
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify(response), 200


@reimbursement_bp.route("/update", methods=["POST"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def update_reimbursement_status():
    data = request.get_json() or {}
    errors = UpdateClaimSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        result = update_claim_status(claim_id=data.get("id"), status=data.get("status"))
        response = {
            "doctorId": result.doctorId,
            "doctorName": result.doctorName,
            "memberId": result.memberId,
            "memberName": result.memberName,
            "departmentId": result.departmentId,
            "departmentName": result.departmentName,
            "status": result.status,
            "amount": result.amount,
            "id": result.id,
        }
    except Exception as e:
        return jsonify({"errors": str(e)}), 400
    return jsonify(response), 200