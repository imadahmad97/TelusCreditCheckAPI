"""
A module for the CreditCardUser class. This class represents a single credit card user and contains
methods to parse dates and create a credit card user.

Classes:
    CreditCardUser: A class to represent a single credit card user.
"""

import datetime
from pydantic import BaseModel


class CreditCardUser(BaseModel):
    """
    A class to represent a single credit card user.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        date_of_birth (str | datetime.date): The date of birth of the user.
        is_existing_customer (bool): A flag indicating if the user is an existing customer.
        credit_card_number (str): The credit card number of the user.
        expiration_date (str | datetime.date): The expiration date of the credit card.
        cvv (str): The CVV of the credit card.
        credit_card_issuer (str): The issuer of the credit card.

    Methods:
        parse_dates()
        create_credit_card_user()
    """

    first_name: str
    last_name: str
    date_of_birth: str | datetime.date
    is_existing_customer: bool
    credit_card_number: str
    expiration_date: str | datetime.date
    cvv: str
    credit_card_issuer: str

    def parse_dates(self):
        """
        Parses the date of birth and expiration date from strings to datetime.date objects.
        """
        self.date_of_birth = datetime.datetime.strptime(
            self.date_of_birth, "%Y-%m-%d"
        ).date()
        expiration_year, expiration_month = map(int, self.expiration_date.split("-"))
        self.expiration_date = datetime.date(expiration_year, expiration_month, 1)

    def create_credit_card_user(self) -> "CreditCardUser":
        """
        Creates a credit card user and parses the dates.

        Returns:
            CreditCardUser: A CreditCardUser object.
        """
        self.parse_dates()
        return self
