"""
This module contains the implementation of the Luhn algorithm for credit card number validation.

Classes:
    LuhnAlgorithmImplementation
    
Dependencies:
    - os: This module provides a way to work with operating system dependent functionality.
    - CreditApprovalRequest: The class representing a credit approval request.
"""

import os
from .credit_approval_request import CreditApprovalRequest


class LuhnAlgorithmImplementation:
    """
    This class contains the implementation of the Luhn algorithm for credit card number validation.

    Methods:
        _separate_digits_by_position(credit_approval_request): Separate credit card number digits
            by position into odd and even digits.
        _double_even_digits(odd_digits): Double the even digits of the credit card number.
        _luhn_reduction_step(doubled_even_digits): Perform the Luhn reduction step on the doubled
            even digits.
        perform_luhn_check_on_credit_approval_request(credit_approval_request): Perform the Luhn
            algorithm check on the credit card number of the credit approval request.
    """

    @staticmethod
    def _separate_digits_by_position(
        credit_approval_request: CreditApprovalRequest,
    ) -> tuple:
        """
        Separate the credit card number digits by position into odd and even digits.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to separate
                the digits from.

        Returns:
            tuple: A tuple containing the odd and even digits of the credit card number.
        """
        raw_odd_digits: list = []
        raw_even_digits: list = []
        i = 1
        while i <= len(credit_approval_request.credit_card_number):
            if i % 2 != 0:
                raw_odd_digits.append(
                    int(credit_approval_request.credit_card_number[-i])
                )
                i += 1
            else:
                raw_even_digits.append(
                    int(credit_approval_request.credit_card_number[-i])
                )
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
    def perform_luhn_check(
        credit_approval_request: CreditApprovalRequest,
    ) -> bool:
        """
        Perform the Luhn algorithm check on the credit card number of the credit approval request.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to check.

        Returns:
            bool: True if the credit card number is valid according to the Luhn algorithm, False
                otherwise.
        """
        odd_digits: list
        even_digits: list
        odd_digits, even_digits = (
            LuhnAlgorithmImplementation._separate_digits_by_position(
                credit_approval_request
            )
        )
        doubled_even_digits: list = (
            LuhnAlgorithmImplementation._double_digits_at_even_positions(even_digits)
        )
        reduced_even_digits: list = LuhnAlgorithmImplementation._reduce_doubled_digits(
            doubled_even_digits
        )
        if (sum(odd_digits) + sum(reduced_even_digits)) % int(
            os.getenv("LUHN_MODULUS")
        ) != 0:
            credit_approval_request.errors += "400: Invalid credit card number; "
            return False
