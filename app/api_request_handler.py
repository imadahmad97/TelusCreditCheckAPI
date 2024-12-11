"""
This module contains the function to handle the credit check request. It runs every time the 
/credit-check route is called.

Functions:
    handle_credit_check_request(credit_approval_request: CreditApprovalRequest) -> dict: Function to
    handle the credit check request.
    
Dependencies:
    - CreditApprovalRequest
    - CreditCardValidator
    - CreditApprovalChecker
"""

from .credit_approval_request import CreditApprovalRequest
from .credit_card_validator import CreditCardValidator
from .credit_approval_checker import CreditApprovalChecker


def handle_credit_check_request(credit_approval_request: CreditApprovalRequest) -> dict:
    """
    Function to handle the credit check request. It formats a credit approval request, validates
    the credit card, and checks the credit approval.

    Parameters:
        credit_approval_request (CreditApprovalRequest): The credit approval request to check the
        approval status of.

    Returns:
        dict: The result of the credit check.
    """
    CreditApprovalRequest.format_credit_approval_request(credit_approval_request)
    CreditCardValidator.validate_credit_card(credit_approval_request)
    if CreditApprovalChecker.check_if_user_approved(credit_approval_request):
        return {"credit_approval": "approved"}
    return {"credit_approval": "denied"}
