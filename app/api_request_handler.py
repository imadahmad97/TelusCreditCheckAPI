"""
This module contains the CreditCheckRequestHandler class, which is responsible for handling the
credit check process for a credit approval request to the API. This class validates the credit card,
credit score, and credit duration of the user in the credit approval request, and returns the result
of the credit check process.

Classes:
    CreditCheckRequestHandler
    
Dependencies:
    - fastapi: The FastAPI framework for building APIs with Python.
    - HTTPException: An exception class to raise HTTP errors.
    - CreditApprovalRequest: The class representing a credit approval request.
    - CreditCardValidator: The class to validate a credit card.
    - DataBaseService: The class to interact with the database.
    - CreditApprovalChecker: The class to check the result of a credit approval request.
"""

import os
from fastapi import HTTPException
from .credit_approval_request import CreditApprovalRequest
from .credit_card_validator import CreditCardValidator
from .database_methods import DataBaseService
from .credit_approval_checker import CreditApprovalChecker
from .luhn_algorithm_validator import LuhnAlgorithmImplementation


class CreditCheckRequestHandler:
    """
    The CreditCheckRequestHandler class is responsible for handling the credit check process for a
    credit approval request to the API. This class validates the credit card, credit score, and
    credit duration of the user in the credit approval request, and returns the result of the credit
    check process.

    Methods:
        _process_credit_approval_request(credit_approval_request): Run the credit check process for
            the credit approval request.
        _return_credit_check_result(credit_approval_request): Return the result of the credit check
            process for the credit approval request.
        process_and_return_credit_check_result(credit_approval_request): Process the credit
            approval request and return the result of the credit

    Dependencies:
        - CreditApprovalRequest: The class representing a credit approval request.
        - CreditCardValidator: The class to validate a credit card.
        - DataBaseService: The class to interact with the database.
        - CreditApprovalChecker: The class to check the result of a credit approval request.
        - LuhnAlgorithmImplementation: The class to perform the Luhn check on a credit card number.
    """

    @staticmethod
    def _process_credit_approval_request(
        credit_approval_request: CreditApprovalRequest,
    ) -> None:
        """
        Run the credit check process for the credit approval request. This includes checking the
        credit card, credit score, and credit duration.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to check.
        """
        CreditApprovalRequest.convert_dob_and_expiration_from_string_to_datetime(
            credit_approval_request
        )

        CreditCardValidator.validate_credit_card(credit_approval_request)

        if os.getenv("RUN_LUHN_CHECK") == "True":
            LuhnAlgorithmImplementation.perform_luhn_check_on_credit_approval_request(
                credit_approval_request
            )

    @staticmethod
    def _return_credit_check_result(
        credit_approval_request: CreditApprovalRequest,
    ) -> dict:
        """
        Return the result of the credit check process for the credit approval request, including
        whether the credit was approved or denied, as well as any errors that occurred.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to check.

        Returns:
            dict: The result of the credit check process.
        """
        if credit_approval_request.errors != "":
            DataBaseService().record_credit_approval_request_transaction(
                credit_approval_request, errors=credit_approval_request.errors
            )
            raise HTTPException(status_code=400, detail=credit_approval_request.errors)

        if CreditApprovalChecker.check_credit_approval_request_result(
            credit_approval_request
        ):
            DataBaseService().record_credit_approval_request_transaction(
                credit_approval_request, approved=True
            )
            return {"credit_approval": "approved"}

        DataBaseService().record_credit_approval_request_transaction(
            credit_approval_request, approved=False
        )
        return {"credit_approval": "denied"}

    @staticmethod
    def process_and_return_credit_check_result(
        credit_approval_request: CreditApprovalRequest,
    ) -> dict:
        """
        Process the credit approval request and return the result of the credit check process.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to check.

        Returns:
            dict: The result of the credit check process.
        """
        CreditCheckRequestHandler._process_credit_approval_request(
            credit_approval_request
        )
        return CreditCheckRequestHandler._return_credit_check_result(
            credit_approval_request
        )
