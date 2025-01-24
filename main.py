"""
This module contains the route for the Telus Credit Check API. It handles POST requests for 
the /check_credit endpoint and uses the handle_credit_check_request function to process the credit 
check request.

Functions:
    credit_check_route(credit_approval_request: Annotated[CreditApprovalRequest, Form()]) -> dict: 
    The API endpoint to check approval status of a credit approval request.

Endpoints:
    /check_credit: The endpoint to check the approval status of a credit approval request.

Dependencies:
    - FastAPI
    - CreditApprovalRequest
    - handle_credit_check_request
"""

from typing import Annotated
from fastapi import Form
import logging
from app.model.credit_approval_request import CreditApprovalRequest
from app.service.credit_check_service import process_credit_check
from create_app import create_app, InitializationError

try:
    app, db_service = create_app()
except ConnectionError as e:
    logging.error("[APP INIT] Failed to initialize connection to Supabase.")
    raise ConnectionError("Failed to initialize connection to Supabase.") from e
except InitializationError as e:
    logging.error("[APP INIT] Failed to initialize FastAPI app.")
    raise InitializationError("Failed to initialize FastAPI app.") from e
except Exception as e:
    logging.error("[APP INIT] Failed to initialize app.")
    raise InitializationError("Failed to initialize app.") from e


@app.post("/check_credit")
def credit_check_route(
    credit_approval_request: Annotated[CreditApprovalRequest, Form()]
) -> dict | str:
    """
    Function with the API endpoint to check the approval status of a credit approval request.

    Parameters:
        credit_approval_request (CreditApprovalRequest): Form data for the credit approval request.

    Returns:
        dict: The result of the credit check.
    """
    return process_credit_check(credit_approval_request, db_service)
