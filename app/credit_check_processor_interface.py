from app.database_service import DataBaseService
from app.credit_approval_request import CreditApprovalRequest
from fastapi import HTTPException
from app.card_validation_interface import validate_credit_card
from app.credit_approval_checker_interface import check_credit_approval_request_result


def credit_check_processor(credit_approval_request: CreditApprovalRequest) -> dict:

    # Step 1: Validate the incoming request
    validate_credit_card(credit_approval_request)

    # Step 2: Fetch the credit score and duration from the database
    credit_score, credit_duration = (
        DataBaseService.fetch_credit_score_and_duration_from_db(credit_approval_request)
    )

    # Step 3: Run the credit check process
    response = check_credit_approval_request_result(
        credit_approval_request, credit_score, credit_duration
    )

    # Step 4: Save the credit approval request to the database
    DataBaseService.record_credit_approval_request_transaction(
        credit_approval_request, approval_status=response
    )

    # Step 5: If applicable, raise an exception with errors
    if credit_approval_request.errors != "":
        raise HTTPException(status_code=400, detail=credit_approval_request.errors)

    # Step 6: Return the response
    return response
