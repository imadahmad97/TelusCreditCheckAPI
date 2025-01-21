import datetime
from typing import Any


class CreditApprovalResponse:
    """
    A class to represent a single credit approval response. This class is used to store the
    response of the credit approval service.

    Attributes:
        is_existing_customer (bool): A flag indicating if the user for whom the credit approval
        request is an existing customer.
        date_of_birth (datetime.date): The date of birth of the user for whom the credit approval is
        requested.
        is_approved (bool): A flag indicating if the credit approval request was approved.
        errors (str): A string containing any errors that occurred during the credit approval process.
        response (str): A string containing the response from the credit approval service.
        credit_card_number (str): The credit card number of the user for whom the credit approval is
        requested.
    """

    def __init__(
        self,
        is_existing_customer: bool,
        date_of_birth: datetime.date,
        is_approved: bool,
        errors: str = "",
        response: str = "",
        credit_card_number: str = "",
    ):
        # Field validation
        self._validate_type("is_existing_customer", is_existing_customer, bool)
        self._validate_type("date_of_birth", date_of_birth, datetime.date)
        self._validate_type("is_approved", is_approved, bool)
        self._validate_type("errors", errors, str)
        self._validate_type("response", response, str)
        self._validate_type("credit_card_number", credit_card_number, str)

        # Assign attributes after validation
        self.is_existing_customer = is_existing_customer
        self.date_of_birth = date_of_birth
        self.is_approved = is_approved
        self.errors = errors
        self.response = response
        self.credit_card_number = credit_card_number

    def _validate_type(self, field_name: str, value: Any, expected_type: type) -> None:
        """Helper function to validate types."""
        if not isinstance(value, expected_type):
            raise TypeError(
                f"'{field_name}' must be of type {expected_type.__name__}, "
                f"but got {type(value).__name__} instead."
            )
