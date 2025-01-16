from app.interface.utility.credit_validation_utils import CreditCardValidator
import datetime


def get_card_validation_errors(
    credit_card_number: str,
    cvv: str,
    expiration_date: datetime.date,
    credit_card_issuer: str,
) -> str:
    """
    Validates the credit card information.

    Parameters:
        credit_approval_request (CreditApprovalRequest): The credit approval request to
        validate.
    """
    # Prep: Initialize validation error list
    validation_errors: list = []

    # Step 1: Validate card number length
    validation_errors.append(
        CreditCardValidator.get_card_number_length_errors(credit_card_number)
    )

    # Step 2: Validate the CVV number length
    validation_errors.append(CreditCardValidator.get_cvv_length_errors(cvv))

    # Step 3: Validate the card expiration date
    validation_errors.append(
        CreditCardValidator.get_card_expired_errors(expiration_date)
    )

    # Step 4: Validate the credit card issuer
    validation_errors.append(
        CreditCardValidator.get_card_issuer_errors(credit_card_issuer)
    )

    # Step 5: Perform the Luhn check
    validation_errors.append(
        CreditCardValidator.get_luhn_validation_errors(credit_card_number)
    )

    # Step 6: Return the validation errors
    return "".join(validation_errors)
