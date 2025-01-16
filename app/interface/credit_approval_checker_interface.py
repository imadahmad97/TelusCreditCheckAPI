"""
This module contains the check_credit_approval_request_result function which is responsible for
serving as the interface for the credit approval checker. It checks the credit approval request
result based on the credit score and duration from the database, and the credit approval request.

Dependencies:
    - datetime: The datetime module from the Python standard library.
    - CreditApprovalChecker: The class representing the credit approval checker.
"""

import datetime
from app.interface.utility.credit_approval_utils import CreditApprovalChecker


def get_credit_approval_request_result(
    date_of_birth: datetime.date,
    is_existing_customer: bool,
    credit_score: int,
    credit_duration: int,
) -> bool:
    """
    This function checks the credit approval request result based on the credit score and duration
    from the database, and the credit approval request.

    Parameters:
        date_of_birth (datetime.date): The date of birth of the creditee.
        is_existing_customer (bool): A boolean indicating if the creditee is an existing customer.
        credit_score (int): The credit score of the creditee.
        credit_duration (int): The credit duration of the creditee.
    """
    # Prep: Initialize the variables
    creditee_is_of_legal_age = CreditApprovalChecker.is_creditee_is_of_legal_age(
        date_of_birth
    )
    credit_score_and_duration_within_approval_limits = CreditApprovalChecker.is_credit_score_and_credit_duration_within_approval_limits(
        credit_score, credit_duration
    )

    # Step 1: Approve the user if they are an existing customer
    if is_existing_customer or (
        creditee_is_of_legal_age and credit_score_and_duration_within_approval_limits
    ):
        return True

    # Step 2: Deny the user if they do not meet the approval criteria
    return False
