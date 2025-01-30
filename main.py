"""
This module contains the API endpoint for checking the approval status of a credit approval request.
It uses the FastAPI framework to create the API endpoint. The API endpoint is a POST request that 
takes in the form data for the credit approval request and returns the result of the credit check.

Routes:
    /check_credit: The API endpoint for checking the approval status of a credit approval request.

Functions:
    credit_check_route: The function that implements the API endpoint for checking the approval 
    status of a credit approval request.

Dependencies:
    - fastapi: The FastAPI framework for building APIs.
    - app.model.credit_approval_request: The model for the credit approval request.
    - app.service.credit_check_service: The service for processing the credit check.
    - app: The module that initializes the database connection.
"""

from typing import Annotated
from fastapi import Form, FastAPI
from app.model.credit_approval_request import CreditApprovalRequest
from app.service.credit_check_service import process_credit_check
from app import init_db

app = FastAPI()
db_service = init_db()


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
