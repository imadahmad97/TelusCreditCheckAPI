"""
This module contains the check_credit_approval_request_result function which is responsible for
serving as the interface for the credit approval checker. It checks the credit approval request
result based on the credit score and duration from the database, and the credit approval request.

Dependencies:
    - CreditApprovalChecker: The class to check if a user is approved based on the credit approval
    criteria.
    - CreditApprovalRequest: The class representing a credit approval request.
"""

from .credit_approval_checker import CreditApprovalChecker
from .credit_approval_request import CreditApprovalRequest


def check_credit_approval_request_result(
    credit_approval_request: CreditApprovalRequest,
    credit_score: int,
    credit_duration: int,
) -> bool:
    """
    This function checks the credit approval request result based on the credit score and duration
    from the database, and the credit approval request.

    Parameters:
        credit_approval_request (CreditApprovalRequest): The credit approval request to check.
        credit_score (int): The credit score from the database.
        credit_duration (int): The credit duration from the database.
    """
    # Prep: Initialize the CreditApprovalChecker
    credit_approval_checker = CreditApprovalChecker()

    # Step 1: Check if the user is an existing customer, and approve them if they are
    if credit_approval_request.is_existing_customer:
        return {"credit_approval": "approved"}

    # Step 2: Check if the user is of legal age and their credit score and credit duration are
    # within the approval limits, and approve them if they are
    if credit_approval_checker.check_if_creditee_is_of_legal_age_from_credit_approval_request(
        credit_approval_request
    ) and credit_approval_checker.check_if_credit_score_and_credit_duration_within_approval_limits(
        credit_score, credit_duration
    ):
        return {"credit_approval": "approved"}

    # Step 3: Deny the user if they do not meet the approval criteria
    return {"credit_approval": "denied"}
