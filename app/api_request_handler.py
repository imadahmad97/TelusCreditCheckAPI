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
    Function to handle the credit check request. It creates a credit card user,
    validates the credit card, and checks the credit approval.

    Parameters:
        user (CreditCardUser): The user to check the credit.

    Returns:
        dict: The result of the credit check.
    """
    CreditApprovalRequest.format_credit_approval_request(credit_approval_request)
    CreditCardValidator.validate_credit_card(credit_approval_request)
    if CreditApprovalChecker.check_if_user_approved(credit_approval_request):
        return {"credit_approval": "approved"}
    return {"credit_approval": "denied"}
