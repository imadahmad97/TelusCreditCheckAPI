"""
This module contains the credit_check_processor function which serves as the interface for the
credit check processor. It validates the incoming credit approval request, fetches the credit score
and duration from the database, runs the credit check process, saves the credit approval request to
the database, and returns the response.

Dependencies:
    - HTTPException: An exception to raise when an HTTP error occurs.
    - DataBaseService: The class to interact with the database.
    - CreditApprovalRequest: The class representing a credit approval request.
    - validate_credit_card: The function to validate the credit card details.
    - check_credit_approval_request_result: The function to check the credit approval request
    result.
"""

from fastapi import HTTPException
from app.utils.database_service import DataBaseService
from .models.credit_approval_request import CreditApprovalRequest
from .card_validation_interface import validate_credit_card
from .credit_approval_checker_interface import (
    check_credit_approval_request_result,
)


def process_credit_check(credit_approval_request: CreditApprovalRequest) -> dict:
    """
    This function serves as the interface for the credit check processor. It validates the incoming
    credit approval request, fetches the credit score and duration from the database, runs the
    credit check process, saves the credit approval request to the database, and returns the
    response.

    Parameters:
        credit_approval_request (CreditApprovalRequest): An instance of the CreditApprovalRequest
        class representing the credit approval request.
    """
    # Prep: Initialize dependencies
    db_service = DataBaseService()

    # Step 1: Validate the incoming request
    validate_credit_card(credit_approval_request)

    # Step 2: Fetch the credit score and duration from the database
    credit_score, credit_duration = db_service.fetch_credit_score_and_duration_from_db(
        credit_approval_request
    )

    # Step 3: Run the credit check process
    response = check_credit_approval_request_result(
        credit_approval_request, credit_score, credit_duration
    )

    # Step 4: Save the credit approval request to the database
    db_service.record_credit_approval_request_transaction(
        credit_approval_request, approval_status=response
    )

    # Step 5a: If applicable, raise an exception with errors
    if credit_approval_request.errors != "":
        raise HTTPException(status_code=400, detail=credit_approval_request.errors)

    # Step 5b: Return the response
    return response
