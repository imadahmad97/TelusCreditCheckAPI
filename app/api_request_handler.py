"""
This module contains the function to handle the credit check request. It runs every time the 
/credit-check route is called.

Functions:
    handle_credit_check_request(user: CreditCardUser) -> dict: Function to handle the credit check 
    request.
    
Dependencies:
    - CreditCardUser
    - CreditCardValidator
    - CreditApprovalChecker
"""

from .credit_card_validator import CreditCardValidator
from .credit_card_user import CreditCardUser
from .credit_approval_checker import CreditApprovalChecker


def handle_credit_check_request(user: CreditCardUser) -> dict:
    """
    Function to handle the credit check request. It creates a credit card user,
    validates the credit card, and checks the credit approval.

    Parameters:
        user (CreditCardUser): The user to check the credit.

    Returns:
        dict: The result of the credit check.
    """
    CreditCardUser.create_credit_card_user(user)
    CreditCardValidator.validate(user)
    if CreditApprovalChecker.check_approval(user):
        return {"credit_approval": "approved"}
    return {"credit_approval": "denied"}
