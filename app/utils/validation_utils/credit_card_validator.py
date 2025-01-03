"""
This module contains the CreditCardValidator class, which is responsible for validating credit card
information. This class validates the credit card number length, expiration date, credit card issuer
and performs the Luhn algorithm check.

Classes:
    CreditCardValidator

Dependencies:
    - datetime: The module supplies classes for manipulating dates and times.
    - CreditApprovalRequest: The class representing a credit approval request.
"""

import datetime
import os
from app.models.credit_approval_request import CreditApprovalRequest


class CreditCardValidator:
    """
    A class to validate credit card information. This class validates the credit card number length,
    expiration date, and credit card issuer.

    Methods:
        validate_card_number_lengths: Validates the length of the credit card number and CVV to be
        16 and 3-4 digits respectively.
        validate_card_expiration_date: Validates the expiration date of the credit card to be in
        the future.
        validate_credit_card_issuer: Validates the credit card issuer to be Visa, MasterCard, or
        American Express.
    """

    @staticmethod
    def validate_card_number_length(
        credit_approval_request: CreditApprovalRequest,
    ) -> None:
        """
        Validates the length of the credit card number to be between 16 and 19 digits, and appends
        the errors to the credit approval request if the length is invalid.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to
            validate.

        """
        if (
            not int(os.getenv("MINIMUM_CREDIT_CARD_NUMBER_LENGTH"))
            <= len(credit_approval_request.credit_card_number)
            <= int(os.getenv("MAXIMUM_CREDIT_CARD_NUMBER_LENGTH"))
        ):
            credit_approval_request.errors += f"Card number must be between {os.getenv("MINIMUM_CREDIT_CARD_NUMBER_LENGTH")} and {os.getenv("MAXIMUM_CREDIT_CARD_NUMBER_LENGTH")} digits; "

    @staticmethod
    def validate_cvv_number_length(
        credit_approval_request: CreditApprovalRequest,
    ) -> None:
        """
        Validates the length of the CVV to be between 3 and 4 digits, and appends the errors to the
        credit approval request if the length is invalid.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to
            validate.
        """
        if (
            not int(os.getenv("MINIMUM_CREDIT_CARD_CVV_LENGTH"))
            <= len(credit_approval_request.cvv)
            <= int(os.getenv("MAXIMUM_CREDIT_CARD_CVV_LENGTH"))
        ):
            credit_approval_request.errors += f"CVV must be {os.getenv('MINIMUM_CREDIT_CARD_CVV_LENGTH')} or {os.getenv('MAXIMUM_CREDIT_CARD_CVV_LENGTH')} digits; "

    @staticmethod
    def validate_card_expiration_date(
        credit_approval_request: CreditApprovalRequest,
    ) -> None:
        """
        Validates the expiration date of the credit card to be in the future, and appends the errors
        to the credit approval request if the card is expired.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to
            validate.
        """
        if credit_approval_request.expiration_date < datetime.date.today():
            credit_approval_request.errors += "Card is expired; "

    @staticmethod
    def validate_credit_card_issuer(
        credit_approval_request: CreditApprovalRequest,
    ) -> None:
        """
        Validates the credit card issuer to be Visa, MasterCard, or American Express, and appends
        the errors to the credit approval request if the issuer is invalid.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to
            validate.
        """
        if credit_approval_request.credit_card_issuer.lower() not in [
            "visa",
            "mastercard",
            "american express",
        ]:
            credit_approval_request.errors += "Invalid credit card issuer; "
