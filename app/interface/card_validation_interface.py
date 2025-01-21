"""
This module contains the get_card_validation_errors function which is responsible for serving as the
interface for the credit card validation. It validates the credit card information and returns the
validation errors.

Dependencies:
    - CreditCardValidator: The class representing the credit card validator.
    - datetime: The datetime module from the Python standard library.
"""

import datetime
from app.interface.utility.credit_validation_utils import CreditCardValidator


def get_card_validation_errors(
    credit_card_number: str,
    cvv: str,
    expiration_date: datetime.date,
    credit_card_issuer: str,
) -> str:
    """
    Validates the credit card information.

    Parameters:
        credit_card_number (str): The credit card number to validate.
        cvv (str): The CVV number to validate.
        expiration_date (datetime.date): The expiration date to validate.
        credit_card_issuer (str): The credit card issuer to validate.
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
