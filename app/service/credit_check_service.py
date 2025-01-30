"""
This module contains the process_credit_check function which serves as the interface for the
credit check processor. It validates the incoming credit approval request, fetches the credit score
and duration from the database, runs the credit check process, saves the credit approval request to
the database, and returns the response.

Dependencies:
    - HTTPException: The exception class for handling HTTP errors.
    - CreditApprovalRequest: The class representing the credit approval request.
    - CreditApprovalResponse: The class representing the credit approval response.
    - get_card_validation_errors: The function that validates the credit card information.
    - get_credit_approval_request_result: The function that runs the credit check process.
"""

from fastapi import HTTPException
from app.model.credit_approval_request import CreditApprovalRequest
from app.model.credit_approval_response import CreditApprovalResponse
from app.interface.card_validation_interface import get_card_validation_errors
from app.interface.credit_approval_checker_interface import (
    get_credit_approval_request_result,
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

    # Prep Step: Initialize credit score and duration from the database
    credit_score, credit_duration = db_service.fetch_credit_score_and_duration_from_db(
        credit_approval_request.credit_card_number
    )

    # Prep Step: Initialize the response object
    credit_approval_response: CreditApprovalResponse = CreditApprovalResponse(
        is_existing_customer=credit_approval_request.is_existing_customer,
        date_of_birth=credit_approval_request.date_of_birth,
        is_approved=False,
        errors="",
    )

    # Step 1: Append validation errors to the response object
    credit_approval_response.errors += get_card_validation_errors(
        credit_approval_request.credit_card_number,
        credit_approval_request.cvv,
        credit_approval_request.expiration_date,
        credit_approval_request.credit_card_issuer,
    )

    # Step 2: Run the credit check process and update the response object
    credit_approval_response.is_approved = get_credit_approval_request_result(
        credit_approval_request.date_of_birth,
        credit_approval_request.is_existing_customer,
        credit_score,
        credit_duration,
    )

    # Step 3: Save the credit approval request to the database
    db_service.record_credit_approval_request_transaction(
        credit_approval_response.credit_card_number,
        credit_approval_response.is_approved,
        credit_approval_response.errors,
    )

    # Step 4a: If applicable, raise an exception with errors
    if credit_approval_response.errors != "":
        raise HTTPException(status_code=400, detail=credit_approval_response.errors)

    # Step 4b: Return the response
    if credit_approval_response.is_approved:
        return {"credit_approval": "approved"}
    return {"credit_approval": "denied"}
