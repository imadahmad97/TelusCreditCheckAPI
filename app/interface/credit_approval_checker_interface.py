"""
This module contains the check_credit_approval_request_result function which is responsible for
serving as the interface for the credit approval checker. It checks the credit approval request
result based on the credit score and duration from the database, and the credit approval request.

Dependencies:
    - CreditApprovalChecker: The class to check if a user is approved based on the credit approval
    criteria.
    - CreditApprovalRequest: The class representing a credit approval request.
"""

from app.interface.utility.credit_approval_utils import CreditApprovalChecker
import datetime


def check_credit_approval_request_result(
    date_of_birth: datetime.date,
    is_existing_customer: bool,
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
    # Prep: Initialize the CreditApprovalChecker and variables
    creditee_is_of_legal_age = CreditApprovalChecker.is_creditee_is_of_legal_age(
        date_of_birth
    )
    credit_score_and_duration_within_approval_limits = CreditApprovalChecker.is_credit_score_and_credit_duration_within_approval_limits(
        credit_score, credit_duration
    )

    # Step 1: Check if the user is an existing customer, and approve them if they are
    if is_existing_customer:
        return True

    # Step 2: Check if the user is of legal age and their credit score and credit duration are
    # within the approval limits, and approve them if they are
    if creditee_is_of_legal_age and credit_score_and_duration_within_approval_limits:
        return True
    # Step 3: Deny the user if they do not meet the approval criteria
    return False
