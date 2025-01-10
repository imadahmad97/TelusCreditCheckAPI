from app.models.credit_approval_response import CreditApprovalResponse
from app.utils.validation_utils import credit_card_validator


def validate_credit_card(
    credit_approval_response: CreditApprovalResponse,
) -> CreditApprovalResponse:
    """
    Validates the credit card information.

    Parameters:
        credit_approval_request (CreditApprovalRequest): The credit approval request to
        validate.
    """
    # Prep: Initialize dependencies
    card_validator = credit_card_validator.CreditCardValidator()
    validation_errors = []

    # Step 1: Validate card number length
    validation_errors.append(
        card_validator.return_card_number_length_errors(credit_approval_response)
    )

    # Step 2: Validate the CVV number length
    validation_errors.append(
        card_validator.return_cvv_length_errors(credit_approval_response)
    )

    # Step 3: Validate the card expiration date
    validation_errors.append(
        card_validator.return_card_expired_errors(credit_approval_response)
    )

    # Step 4: Validate the credit card issuer
    validation_errors.append(
        card_validator.return_card_issuer_errors(credit_approval_response)
    )

    # Step 5: Perform the Luhn check
    validation_errors.append(
        card_validator.return_luhn_validation_errors(credit_approval_response)
    )

    # Step 6: Create and return the credit approval response
    validated_response = CreditApprovalResponse(
        is_existing_customer=credit_approval_response.is_existing_customer,
        date_of_birth=credit_approval_response.date_of_birth,
        is_approved=False,
        errors="".join(validation_errors),
        response="",
        credit_card_number=credit_approval_response.credit_card_number,
    )

    return validated_response
