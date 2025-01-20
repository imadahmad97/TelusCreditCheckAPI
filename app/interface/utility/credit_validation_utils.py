"""
This module contains the CreditCardValidator class, which is responsible for validating credit card
information. This class validates the credit card number length, expiration date, credit card issuer
and performs the Luhn algorithm check.

Classes:
    CreditCardValidator

Dependencies:
    - datetime: The module supplies classes for manipulating dates and times.
"""

import logging
import datetime
import os


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
    def get_card_number_length_errors(credit_card_number: str) -> str:
        """
        Validates the length of the credit card number to be between 16 and 19 digits, and appends
        the errors to the credit approval request if the length is invalid.

        Parameters:
            credit_card_number (str): The credit card number to validate.
        """
        if (
            not int(os.getenv("MINIMUM_CREDIT_CARD_NUMBER_LENGTH", "8"))
            <= len(credit_card_number)
            <= int(os.getenv("MAXIMUM_CREDIT_CARD_NUMBER_LENGTH", "19"))
        ):
            return f"Card number must be between {os.getenv("MINIMUM_CREDIT_CARD_NUMBER_LENGTH")} and {os.getenv("MAXIMUM_CREDIT_CARD_NUMBER_LENGTH")} digits; "

        return ""

    @staticmethod
    def get_cvv_length_errors(
        cvv: str,
    ) -> str:
        """
        Validates the length of the CVV to be between 3 and 4 digits, and appends the errors to the
        credit approval request if the length is invalid.

        Parameters:
            cvv (str): The CVV number to validate.
        """
        if (
            not int(os.getenv("MINIMUM_CREDIT_CARD_CVV_LENGTH", "3"))
            <= len(cvv)
            <= int(os.getenv("MAXIMUM_CREDIT_CARD_CVV_LENGTH", "4"))
        ):
            return f"CVV must be {os.getenv('MINIMUM_CREDIT_CARD_CVV_LENGTH')} or {os.getenv('MAXIMUM_CREDIT_CARD_CVV_LENGTH')} digits; "

        return ""

    @staticmethod
    def get_card_expired_errors(
        expiration_date: datetime.date,
    ) -> str:
        """
        Validates the expiration date of the credit card to be in the future, and appends the errors
        to the credit approval request if the card is expired.

        Parameters:
            expiration_date (datetime.date): The expiration date to validate.
        """
        if expiration_date < datetime.date.today():
            return "Card is expired; "

        return ""

    @staticmethod
    def get_card_issuer_errors(
        credit_card_issuer: str,
    ) -> str:
        """
        Validates the credit card issuer to be Visa, MasterCard, or American Express, and appends
        the errors to the credit approval request if the issuer is invalid.

        Parameters:
            credit_card_issuer (str): The credit card issuer to validate.
        """
        if credit_card_issuer.lower() not in [
            "visa",
            "mastercard",
            "american express",
        ]:
            return "Invalid credit card issuer type; "

        return ""

    @staticmethod
    def _separate_digits_by_position(
        credit_card_number: str,
    ) -> tuple:
        """
        Separate the credit card number digits by position into odd and even digits.

        Parameters:
            credit_card_number (str): The credit card number to separate.

        Returns:
            tuple: A tuple containing the odd and even digits of the credit card number.
        """
        raw_odd_digits: list = []
        raw_even_digits: list = []
        i = 1
        while i <= len(credit_card_number):
            if i % 2 != 0:
                raw_odd_digits.append(int(credit_card_number[-i]))
                i += 1
            else:
                raw_even_digits.append(int(credit_card_number[-i]))
                i += 1

        return raw_odd_digits, raw_even_digits

    @staticmethod
    def _double_digits_at_even_positions(even_digits: list) -> list:
        """
        Double the even digits of the credit card number.

        Parameters:
            even_digits (list): The list of odd digits of the credit card number.

        Returns:
            list: The list of doubled even digits of the credit card number."""
        doubled_even_digits: list = []
        for digit in even_digits:
            doubled_even_digits.append(digit * 2)
        return doubled_even_digits

    @staticmethod
    def _reduce_doubled_digits(
        doubled_even_digits: list,
    ) -> list:
        """
        Perform the Luhn reduction step on the doubled even digits.

        Parameters:
            doubled_even_digits (list): The list of doubled even digits of the credit card number.

        Returns:
            list: The list of reduced even digits after the Luhn reduction step.
        """
        reduced_even_digits: list = []
        for number in doubled_even_digits:
            if len(str(number)) == 2:
                reduced_number: int = int(str(number)[0]) + int(str(number)[1])
                reduced_even_digits.append(reduced_number)
            else:
                reduced_even_digits.append(number)
        return reduced_even_digits

    @staticmethod
    def get_luhn_validation_errors(
        credit_card_number: str,
    ) -> str:
        """
        Perform the Luhn algorithm check on the credit card number of the credit approval request.

        Parameters:
            credit_card_number (str): The credit card number to validate.

        Returns:
            bool: True if the credit card number is valid according to the Luhn algorithm, False
                otherwise.
        """
        if not isinstance(credit_card_number, str):
            logging.error(
                "Invalid type for credit_card_number: Expected str, got %s",
                type(credit_card_number).__name__,
            )
            return "Invalid credit card number type; "

        odd_digits: list
        even_digits: list
        odd_digits, even_digits = CreditCardValidator._separate_digits_by_position(
            credit_card_number
        )
        doubled_even_digits: list = (
            CreditCardValidator._double_digits_at_even_positions(even_digits)
        )
        reduced_even_digits: list = CreditCardValidator._reduce_doubled_digits(
            doubled_even_digits
        )
        if (sum(odd_digits) + sum(reduced_even_digits)) % int(
            os.getenv("LUHN_MODULUS", "10")
        ) != 0:
            return "Invalid credit card number; "

        return ""
