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

import os
from fastapi import HTTPException
from app.service.database_service import DataBaseService
from app.model.credit_approval_request import CreditApprovalRequest
from app.model.credit_approval_response import CreditApprovalResponse
from app.interface.card_validation_interface import validate_credit_card
from app.interface.credit_approval_checker_interface import (
    check_credit_approval_request_result,
)


def process_credit_check(credit_approval_request: CreditApprovalRequest) -> str:
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
    db_service = DataBaseService(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

    # Step 1: Validate the incoming request
    validated_response: CreditApprovalResponse = validate_credit_card(
        credit_approval_request
    )

    # Step 2: Fetch the credit score and duration from the database
    credit_score: int
    credit_duration: int
    credit_score, credit_duration = db_service.fetch_credit_score_and_duration_from_db(
        credit_approval_request
    )

    # Step 3: Run the credit check process
    processed_response: CreditApprovalResponse = check_credit_approval_request_result(
        validated_response, credit_score, credit_duration
    )

    # Step 4: Save the credit approval request to the database
    db_service.record_credit_approval_request_transaction(processed_response)

    # Step 5a: If applicable, raise an exception with errors
    if processed_response.errors != "":
        raise HTTPException(status_code=400, detail=processed_response.errors)

    # Step 5b: Return the response
    return processed_response.response
