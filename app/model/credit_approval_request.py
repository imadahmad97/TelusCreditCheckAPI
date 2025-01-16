import datetime
from pydantic import BaseModel


class CreditApprovalRequest(BaseModel):
    """
    A class to represent a single credit approval request.

    Attributes:
        first_name (str): The first name of the user for whom the credit approval is requested.
        last_name (str): The last name of the user for whom the credit approval is requested.
        is_existing_customer (bool): A flag indicating if the user for whom the credit approval
        request is an existing customer.
        credit_card_number (str): The credit card number of the user for whom the credit approval
        is requested.
        cvv (str): The CVV of the credit card of the user for whom the credit approval is requested.
        credit_card_issuer (str): The issuer of the credit card of the user for whom the credit
        approval is requested.
        date_of_birth (datetime.date): The date of birth of the user for whom the credit approval is
        requested.
        expiration_date (datetime.date): The expiration date of the credit card of the user for whom
        the credit approval is requested.

    Methods:
        date_of_birth (property): The date of birth of the user for whom the credit approval is
        requested.
        expiration_date (property): The expiration date of the credit card of the user for whom the
        credit approval is requested.
    """

    first_name: str
    last_name: str
    is_existing_customer: bool
    credit_card_number: str
    cvv: str
    credit_card_issuer: str

    _date_of_birth: datetime.date
    _expiration_date: datetime.date

    def __init__(self, **data):
        super().__init__(**data)
        self.date_of_birth = data.get("date_of_birth")
        self.expiration_date = data.get("expiration_date")

    @property
    def date_of_birth(self) -> datetime.date:
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value: str | datetime.date) -> None:
        if isinstance(value, str):
            self._date_of_birth = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        elif isinstance(value, datetime.date):
            self._date_of_birth = value
        else:
            raise ValueError("Invalid type for date_of_birth")

    @property
    def expiration_date(self) -> datetime.date:
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, value: str | datetime.date) -> None:
        if isinstance(value, str):
            expiration_year, expiration_month = map(int, value.split("-"))
            self._expiration_date = datetime.date(expiration_year, expiration_month, 1)
        elif isinstance(value, datetime.date):
            self._expiration_date = value
        else:
            raise ValueError("Invalid type for expiration_date")
