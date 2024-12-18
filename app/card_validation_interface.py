from .credit_approval_request import CreditApprovalRequest
from .credit_card_validator import CreditCardValidator
from .luhn_algorithm_validator import LuhnAlgorithmImplementation


def validate_credit_card(credit_approval_request: CreditApprovalRequest) -> None:
    """
    Validates the credit card information.

    Parameters:
        credit_approval_request (CreditApprovalRequest): The credit approval request to
        validate.
    """
    # Prep: Initialize dependencies
    credit_card_validator = CreditCardValidator()
    luhn_validator = LuhnAlgorithmImplementation()

    # Step 1: Validate all card number lengths
    credit_card_validator.validate_card_number_lengths(credit_approval_request)

    # Step 2: Validate the card expiration date
    credit_card_validator.validate_card_expiration_date(credit_approval_request)

    # Step 3: Validate the credit card issuer
    credit_card_validator.validate_credit_card_issuer(credit_approval_request)

    # Step 4: Perform the Luhn check
    luhn_validator.perform_luhn_check(credit_approval_request)
