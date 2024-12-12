from .credit_approval_request import CreditApprovalRequest
from fastapi import HTTPException


class LuhnAlgorithmImplementation:
    @staticmethod
    def _split_odd_and_even_digits(
        credit_approval_request: CreditApprovalRequest,
    ) -> tuple:
        raw_odd_digits = []
        raw_even_digits = []
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
    def _double_even_digits(odd_digits: list) -> list:
        doubled_even_digits = []
        for digit in odd_digits:
            doubled_even_digits.append(digit * 2)
        return doubled_even_digits

    @staticmethod
    def _perform_luhn_reduction_step_on_doubled_even_digits(
        doubled_even_digits: list,
    ) -> list:
        reduced_even_digits = []
        for number in doubled_even_digits:
            if len(str(number)) == 2:
                reduced_number = int(str(number)[0]) + int(str(number)[1])
                reduced_even_digits.append(reduced_number)
            else:
                reduced_even_digits.append(number)
        return reduced_even_digits

    @staticmethod
    def perform_luhn_check_on_credit_approval_request(
        credit_approval_request: CreditApprovalRequest,
    ) -> bool:
        odd_digits, even_digits = (
            LuhnAlgorithmImplementation._split_odd_and_even_digits(
                credit_approval_request
            )
        )
        doubled_even_digits = LuhnAlgorithmImplementation._double_even_digits(
            even_digits
        )
        reduced_even_digits = LuhnAlgorithmImplementation._perform_luhn_reduction_step_on_doubled_even_digits(
            doubled_even_digits
        )
        if (sum(odd_digits) + sum(reduced_even_digits)) % 10 != 0:
            raise HTTPException(status_code=400, detail="Credit card number is invalid")
