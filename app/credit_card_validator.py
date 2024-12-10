"""
A module to validate credit card information. It contains the CreditCardValidator class with methods
to validate the credit card number, expiration date, and issuer.

Classes:
    CreditCardValidator: A class to validate credit card information.
    
Dependencies:
    - datetime
    - HTTPException
    - CreditCardUser
"""

import datetime
from fastapi import HTTPException
from .credit_card_user import CreditCardUser


class CreditCardValidator:
    """
    A class to validate credit card information.

    Methods:
        validate_number_lengths(credit_card_user: CreditCardUser): Validates the length of the
        credit card number and CVV.
        validate_expiration_date(credit_card_user: CreditCardUser): Validates the expiration date of
        the credit card.
        validate_credit_card_issuer(credit_card_user: CreditCardUser): Validates the credit card
        issuer.
        validate(credit_card_user: CreditCardUser) -> bool: Validates the credit card information by
        running all the validation methods.
    """

    @staticmethod
    def validate_number_lengths(credit_card_user: CreditCardUser):
        """
        Validates the length of the credit card number and CVV to be 16 and 3-4 digits respectively.

        Parameters:
            credit_card_user (CreditCardUser): The credit card user to validate.

        Raises:
            HTTPException: If the credit card number is not 16 digits or the CVV is not 3-4 digits.
        """
        if len(credit_card_user.credit_card_number) != 16:
            raise HTTPException(status_code=400, detail="Card number must be 16 digits")
        if not 3 <= len(credit_card_user.cvv) <= 4:
            raise HTTPException(status_code=400, detail="CVV must be 3 or 4 digits")

    @staticmethod
    def validate_expiration_date(credit_card_user: CreditCardUser):
        """
        Validates the expiration date of the credit card to be in the future.

        Parameters:
            credit_card_user (CreditCardUser): The credit card user to validate.

        Raises:
            HTTPException: If the credit card is expired.
        """
        if credit_card_user.expiration_date < datetime.date.today():
            raise HTTPException(status_code=400, detail="Card is expired")

    @staticmethod
    def validate_credit_card_issuer(credit_card_user: CreditCardUser):
        """
        Validates the credit card issuer to be Visa, MasterCard, or American Express.

        Parameters:
            credit_card_user (CreditCardUser): The credit card user to validate.

        Raises:
            HTTPException: If the credit card issuer is not Visa, MasterCard, or American Express.
        """
        if credit_card_user.credit_card_issuer.lower() not in [
            "visa",
            "mastercard",
            "american express",
        ]:
            raise HTTPException(status_code=400, detail="Invalid credit card issuer")

    @staticmethod
    def validate(credit_card_user: CreditCardUser):
        """
        Validates the credit card information by running all the validation methods.

        Parameters:
            credit_card_user (CreditCardUser): The credit card user to validate.

        Returns:
            bool: True if the credit card information is valid.
        """
        CreditCardValidator.validate_number_lengths(credit_card_user)
        CreditCardValidator.validate_expiration_date(credit_card_user)
        CreditCardValidator.validate_credit_card_issuer(credit_card_user)
        return True
