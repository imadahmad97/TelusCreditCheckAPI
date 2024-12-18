from .credit_approval_checker import CreditApprovalChecker


def check_credit_approval_request_result(
    credit_approval_request, credit_score, credit_duration
) -> bool:
    # Prep: Initialize the CreditApprovalChecker
    credit_approval_checker = CreditApprovalChecker()

    # Step 1: Check if the user is an existing customer, and approve them if they are
    if credit_approval_request.is_existing_customer:
        return {"credit_approval": "approved"}

    # Step 2: Check if the user is of legal age and their credit score and credit duration are
    # within the approval limits, and approve them if they are
    if credit_approval_checker._check_if_creditee_is_of_legal_age_from_credit_approval_request(
        credit_approval_request
    ) and credit_approval_checker._check_if_credit_score_and_credit_duration_within_approval_limits(
        credit_approval_request, credit_score, credit_duration
    ):
        return {"credit_approval": "approved"}
    return {"credit_approval": "denied"}
