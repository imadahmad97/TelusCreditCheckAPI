"""
A module for the CreditApprovalRequest class. This class represents a single credit approval request
and contains methods to parse dates and create a credit approval request.

Classes:
    CreditApprovalRequest: A class to represent a single credit approval request.

Dependencies:
    - datetime
    - pydantic
"""

import datetime
from pydantic import BaseModel


class CreditApprovalRequest(BaseModel):
    """
    A class to represent a single credit approval request.

    Attributes:
        first_name (str): The first name of the user for whom the credit approval is requested.
        last_name (str): The last name of the user for whom the credit approval is requested.
        date_of_birth (str | datetime.date): The date of birth of the user for whom the credit
        approval is requested.
        is_existing_customer (bool): A flag indicating if the user for whom the credit approval
        request is an existing customer.
        credit_card_number (str): The credit card number of the user for whom the credit approval
        is requested.
        expiration_date (str | datetime.date): The expiration date of the credit card of the user
        for whom the credit approval is requested.
        cvv (str): The CVV of the credit card of the user for whom the credit approval is requested.
        credit_card_issuer (str): The issuer of the credit card of the user for whom the credit
        approval is requested.
        errors (str): The errors that occurred during the credit approval request.

    Methods:
        convert_dob_and_expiration_from_string_to_datetime: Parses the date of birth and expiration
        date in the credit approval request from strings to datetime.date objects.
    """

    first_name: str
    last_name: str
    date_of_birth: str | datetime.date
    is_existing_customer: bool
    credit_card_number: str
    expiration_date: str | datetime.date
    cvv: str
    credit_card_issuer: str
    errors: str = ""

    def convert_dob_and_expiration_from_string_to_datetime(self):
        """
        Parses the date of birth and expiration date in the credit approval request from strings to
        datetime.date objects.
        """
        self.date_of_birth = datetime.datetime.strptime(
            self.date_of_birth, "%Y-%m-%d"
        ).date()
        expiration_year, expiration_month = map(int, self.expiration_date.split("-"))
        self.expiration_date = datetime.date(expiration_year, expiration_month, 1)
