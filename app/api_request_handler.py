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
from .luhn_algorithm_valdiator import LuhnAlgorithmImplementation
from .database_transaction_recorder import DatabaseTransactionRecorder
from .credit_approval_checker import CreditApprovalChecker
from fastapi import HTTPException


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

    CreditCardValidator.validate_credit_card_from_credit_approval_request(
        credit_approval_request
    )

    LuhnAlgorithmImplementation.perform_luhn_check_on_credit_approval_request(
        credit_approval_request
    )

    if credit_approval_request.errors != "":
        print(credit_approval_request.errors)
        raise HTTPException(status_code=400, detail=credit_approval_request.errors)

    if CreditApprovalChecker.check_credit_approval_request_result(
        credit_approval_request
    ):
        DatabaseTransactionRecorder().record_transaction(
            credit_approval_request, approved=True
        )
        return {"credit_approval": "approved"}

    DatabaseTransactionRecorder().record_transaction(
        credit_approval_request, approved=False
    )
    return {"credit_approval": "denied"}
