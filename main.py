"""
This module contains the route for the Telus Credit Check API. It handles GET requests for 
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
from fastapi import FastAPI, Form
from app.credit_approval_request import CreditApprovalRequest
from app.api_request_handler import CreditCheckRequestHandler

app = FastAPI()


@app.post("/check_credit")
def credit_check_route(
    credit_approval_request: Annotated[CreditApprovalRequest, Form()]
) -> dict:
    """
    Function with the API endpoint to check the approval status of a credit approval request.

    Parameters:
        credit_approval_request (CreditApprovalRequest): Form data for the credit approval request.

    Returns:
        dict: The result of the credit check.
    """
    return CreditCheckRequestHandler.process_and_return_credit_check_result(
        credit_approval_request
    )
