from app.credit_card_validator import CreditCardValidator
from app.credit_approval_checker import CreditApprovalChecker
from app.database_service import DataBaseService
from app.credit_approval_request import CreditApprovalRequest
from fastapi import HTTPException


def credit_check_processor(credit_approval_request: CreditApprovalRequest) -> dict:

    # Prep: Initialize dependencies
    credit_card_validator = CreditCardValidator()
    credit_approval_checker = CreditApprovalChecker()
    db_service = DataBaseService()

    # Step 1: Validate the incoming request
    credit_card_validator.validate_credit_card(credit_approval_request)

    # Step 2: Fetch the credit score and duration from the database

    credit_score: int = db_service.check_credit_score_for_credit_approval_request(
        credit_approval_request
    )
    credit_duration: int = db_service.check_credit_duration_for_credit_approval_request(
        credit_approval_request
    )

    # Step 3: Run the credit check process
    response = credit_approval_checker.check_credit_approval_request_result(
        credit_approval_request, credit_score, credit_duration
    )

    # Step 4: Save the credit approval request to the database
    db_service.record_credit_approval_request_transaction(
        credit_approval_request, approval_status=response
    )

    # Step 5: Return the response
    if credit_approval_request.errors != "":
        raise HTTPException(status_code=400, detail=credit_approval_request.errors)

    if response:
        return {"credit_approval": "approved"}
    return {"credit_approval": "denied"}
