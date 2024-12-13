"""
This module contains the CreditCardValidator class, which is responsible for validating credit card
information. This class validates the credit card number length, expiration date, credit card issuer
and performs the Luhn algorithm check.

Classes:
    CreditCardValidator

Dependencies:
    - datetime: The module supplies classes for manipulating dates and times.
    - CreditApprovalRequest: The class representing a credit approval request.
    - LuhnAlgorithmImplementation: The class to perform the Luhn algorithm check.
"""

import datetime
from .credit_approval_request import CreditApprovalRequest
from .luhn_algorithm_valdiator import LuhnAlgorithmImplementation


class CreditCardValidator:
    """
    A class to validate credit card information. This class validates the credit card number length,
    expiration date, credit card issuer, and performs the Luhn algorithm check.

    Methods:
        _validate_card_number_lengths_from_credit_approval_request(credit_approval_request):
            Validates the length of the credit card number and CVV to be 16 and 3-4 digits
            respectively, and appends the errors to the credit approval request if the length(s) are
            invalid.
        _validate_card_expiration_date_from_credit_approval_request(credit_approval_request):
            Validates the expiration date of the credit card to be in the future, and appends the
            errors to the credit approval request if the card is expired.
        _validate_credit_card_issuer_from_credit_approval_request(credit_approval_request):
            Validates the credit card issuer to be Visa, MasterCard, or American Express, and
            appends the errors to the credit approval request if the issuer is invalid.
        validate_credit_card_from_credit_approval_request(credit_approval_request): Validates the
            credit card information by running all the validation methods, including validating the
            card number length, expiration date, credit card issuer, and performing the Luhn
            algorithm check.
    """

    @staticmethod
    def _validate_card_number_lengths_from_credit_approval_request(
        credit_approval_request: CreditApprovalRequest,
    ):
        """
        Validates the length of the credit card number and CVV to be 16 and 3-4 digits respectively,
        and appends the errors to the credit approval request if the length(s) are invalid.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to
            validate.
        """
        if not 8 <= len(credit_approval_request.credit_card_number) <= 19:
            credit_approval_request.errors += (
                "400: Card number must be between 8 and 19 digits; "
            )
        if not 3 <= len(credit_approval_request.cvv) <= 4:
            credit_approval_request.errors += "400: CVV must be 3 or 4 digits; "

    @staticmethod
    def _validate_card_expiration_date_from_credit_approval_request(
        credit_approval_request: CreditApprovalRequest,
    ):
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
    def _validate_credit_card_issuer_from_credit_approval_request(
        credit_approval_request: CreditApprovalRequest,
    ):
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
    def validate_credit_card_from_credit_approval_request(
        credit_approval_request: CreditApprovalRequest,
    ):
        """
        Validates the credit card information by running all the validation methods, including
        validating the card number length, expiration date, credit card issuer, and performing the
        Luhn algorithm check.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to
            validate.

        Returns:
            bool: True if the credit card information is valid.
        """
        CreditCardValidator._validate_card_number_lengths_from_credit_approval_request(
            credit_approval_request
        )
        CreditCardValidator._validate_card_expiration_date_from_credit_approval_request(
            credit_approval_request
        )
        CreditCardValidator._validate_credit_card_issuer_from_credit_approval_request(
            credit_approval_request
        )
        LuhnAlgorithmImplementation.perform_luhn_check_on_credit_approval_request(
            credit_approval_request
        )
        return True
