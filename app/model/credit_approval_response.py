import datetime


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
        # Collect all fields and their expected types in one place
        fields = {
            "is_existing_customer": (is_existing_customer, bool),
            "date_of_birth": (date_of_birth, datetime.date),
            "is_approved": (is_approved, bool),
            "errors": (errors, str),
            "response": (response, str),
            "credit_card_number": (credit_card_number, str),
        }

        # Validate each field against its expected type
        for field_name, (value, expected_type) in fields.items():
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"'{field_name}' must be of type {expected_type.__name__}, "
                    f"but got {type(value).__name__} instead."
                )

        # Once valid, assign them to the instance
        for field_name, (value, _) in fields.items():
            setattr(self, field_name, value)
