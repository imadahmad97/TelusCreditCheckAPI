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
from .credit_approval_request import CreditApprovalRequest
from .luhn_algorithm_validator import LuhnAlgorithmImplementation


class CreditCardValidator:
    """
    The CreditCardValidator class is responsible for validating credit card information. This class
    validates the credit card number length, expiration date, credit card issuer, and performs the
    Luhn algorithm check.

    Methods:
        _validate_card_number_lengths(credit_approval_request): Validates the length of the credit
            card number and CVV to be 16 and 3-4 digits respectively.
        _validate_card_expiration_date(credit_approval_request): Validates the expiration date of
            the credit card to be in the future.
        _validate_credit_card_issuer(credit_approval_request): Validates the credit card issuer to
            be Visa, MasterCard, or American Express.
        validate_credit_card(credit_approval_request): Validates the credit card information
    """

    @staticmethod
    def _validate_card_number_lengths(
        credit_approval_request: CreditApprovalRequest,
    ) -> None:
        """
        Validates the length of the credit card number and CVV to be 16 and 3-4 digits respectively,
        and appends the errors to the credit approval request if the length(s) are invalid.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to
            validate.
        """
        if (
            not int(os.getenv("MINIMUM_CREDIT_CARD_NUMBER_LENGTH"))
            <= len(credit_approval_request.credit_card_number)
            <= int(os.getenv("MAXIMUM_CREDIT_CARD_NUMBER_LENGTH"))
        ):
            credit_approval_request.errors += f"400: Card number must be between {os.getenv("MINIMUM_CREDIT_CARD_NUMBER_LENGTH")} and {os.getenv("MAXIMUM_CREDIT_CARD_NUMBER_LENGTH")} digits; "
            print(credit_approval_request.errors)
        if (
            not int(os.getenv("MINIMUM_CREDIT_CARD_CVV_LENGTH"))
            <= len(credit_approval_request.cvv)
            <= int(os.getenv("MAXIMUM_CREDIT_CARD_CVV_LENGTH"))
        ):
            credit_approval_request.errors += f"400: CVV must be {os.getenv('MINIMUM_CREDIT_CARD_CVV_LENGTH')} or {os.getenv('MAXIMUM_CREDIT_CARD_CVV_LENGTH')} digits; "

    @staticmethod
    def _validate_card_expiration_date(
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
            credit_approval_request.errors += "400: Card is expired; "

    @staticmethod
    def _validate_credit_card_issuer(
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
            credit_approval_request.errors += "400: Invalid credit card issuer; "

    @staticmethod
    def validate_credit_card(
        credit_approval_request: CreditApprovalRequest,
    ) -> None:
        """
        Validates the credit card information by running all the validation methods, including
        validating the card number length, expiration date, credit card issuer, and performing the
        Luhn algorithm check.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to
            validate.
        """
        CreditCardValidator._validate_card_number_lengths(credit_approval_request)
        CreditCardValidator._validate_card_expiration_date(credit_approval_request)
        CreditCardValidator._validate_credit_card_issuer(credit_approval_request)
        LuhnAlgorithmImplementation.perform_luhn_check(credit_approval_request)
