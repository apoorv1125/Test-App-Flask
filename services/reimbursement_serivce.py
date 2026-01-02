from repository.reimbursement.ReimbursementRepo import ReimbursementRepo

def create_claim(dataModel):
    return ReimbursementRepo().create_claim(dataModel)

def delete_claim(claim_id):
    return ReimbursementRepo().delete_claim(claim_id)

def reimbursement_all_list_service():
    return ReimbursementRepo().get_all_reimbursements()

def individual_reimbursement_service(claim_id):
    return ReimbursementRepo().get_reimbursements(claim_id)

def update_claim_status(claim_id, status):
    return ReimbursementRepo().update_claim_status(claim_id, status)