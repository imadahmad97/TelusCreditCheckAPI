"""
This module contains the credit_check_processor function which serves as the interface for the
credit check processor. It validates the incoming credit approval request, fetches the credit score
and duration from the database, runs the credit check process, saves the credit approval request to
the database, and returns the response.

Dependencies:
    - HTTPException: An exception to raise when an HTTP error occurs.
    - CreditApprovalRequest: The class representing a credit approval request.
    - validate_credit_card: The function to validate the credit card details.
    - check_credit_approval_request_result: The function to check the credit approval request
    result.
"""

from fastapi import HTTPException
from app.model.credit_approval_request import CreditApprovalRequest
from app.model.credit_approval_response import CreditApprovalResponse
from app.interface.card_validation_interface import get_card_validation_errors
from app.interface.credit_approval_checker_interface import (
    check_credit_approval_request_result,
)


def process_credit_check(
    credit_approval_request: CreditApprovalRequest, db_service
) -> dict[str, str]:
    """
    This function serves as the interface for the credit check processor. It validates the incoming
    credit approval request, fetches the credit score and duration from the database, runs the
    credit check process, saves the credit approval request to the database, and returns the
    response.

    Parameters:
        credit_approval_request (CreditApprovalRequest): An instance of the CreditApprovalRequest
        class representing the credit approval request.
        db_service: The database service object.
    """

    # Prep Step: Initialize the response object and variables
    credit_card_number = credit_approval_request.credit_card_number
    cvv = credit_approval_request.cvv
    expiration_date = credit_approval_request.expiration_date
    date_of_birth = credit_approval_request.date_of_birth
    credit_card_issuer = credit_approval_request.credit_card_issuer
    is_existing_customer = credit_approval_request.is_existing_customer

    credit_approval_response: CreditApprovalResponse = CreditApprovalResponse(
        is_existing_customer=is_existing_customer,
        date_of_birth=date_of_birth,
        is_approved=False,
        errors="",
    )

    # Step 1: Validate the incoming request
    credit_approval_response.errors += get_card_validation_errors(
        credit_card_number, cvv, expiration_date, credit_card_issuer
    )

    # Step 2: Fetch the credit score and duration from the database
    credit_score: int
    credit_duration: int
    credit_score, credit_duration = db_service.fetch_credit_score_and_duration_from_db(
        credit_card_number
    )

    # Step 3: Run the credit check process
    credit_approval_response.is_approved = check_credit_approval_request_result(
        date_of_birth, is_existing_customer, credit_score, credit_duration
    )

    # Step 4: Save the credit approval request to the database
    db_service.record_credit_approval_request_transaction(
        credit_approval_response.credit_card_number,
        credit_approval_response.is_approved,
        credit_approval_response.errors,
    )

    # Step 5a: If applicable, raise an exception with errors
    if credit_approval_response.errors != "":
        raise HTTPException(status_code=400, detail=credit_approval_response.errors)

    # Step 5b: Return the response
    if credit_approval_response.is_approved:
        return {"credit_approval": "approved"}
    return {"credit_approval": "denied"}
