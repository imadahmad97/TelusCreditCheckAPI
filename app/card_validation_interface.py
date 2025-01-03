from app.models.credit_approval_request import CreditApprovalRequest
from app.utils.validation_utils import credit_card_validator
from .utils.validation_utils.luhn_algorithm_validator import LuhnAlgorithmImplementation


def validate_credit_card(credit_approval_request: CreditApprovalRequest) -> None:
    """
    Validates the credit card information.

    Parameters:
        credit_approval_request (CreditApprovalRequest): The credit approval request to
        validate.
    """
    # Prep: Initialize dependencies
    card_validator = credit_card_validator.CreditCardValidator()
    luhn_validator = LuhnAlgorithmImplementation()

    # Step 1: Validate card number length
    card_validator.validate_card_number_length(credit_approval_request)

    # Step 2: Validate the CVV number length
    card_validator.validate_cvv_number_length(credit_approval_request)

    # Step 3: Validate the card expiration date
    card_validator.validate_card_expiration_date(credit_approval_request)

    # Step 4: Validate the credit card issuer
    card_validator.validate_credit_card_issuer(credit_approval_request)

    # Step 5: Perform the Luhn check
    luhn_validator.perform_luhn_check(credit_approval_request)
