"""
This module contains the route for the Telus Credit Check API. It handles GET requests for 
the /check_credit endpoint and uses the handle_credit_check_request function to process the credit 
check request.

Functions:
    credit_check_route(credit_approval_request: Annotated[CreditApprovalRequest, Form()]) -> dict: 
    The API endpoint to check the credit of a user.

Endpoints:
    /check_credit: The endpoint to check the credit of a credit approval request.

Dependencies:
    - FastAPI
    - CreditApprovalRequest
    - handle_credit_check_request
"""

from typing import Annotated
from fastapi import FastAPI, Form
from app.credit_approval_request import CreditApprovalRequest
from app.api_request_handler import handle_credit_check_request

app = FastAPI()


@app.post("/check_credit")
def credit_check_route(
    credit_approval_request: Annotated[CreditApprovalRequest, Form()]
) -> dict:
    """
    Function with the API endpoint to check the credit of a user.

    Parameters:
        user (CreditCardUser): The form data of the user to check the credit.

    Returns:
        dict: The result of the credit check.
    """
    return handle_credit_check_request(credit_approval_request)
