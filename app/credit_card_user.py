from pydantic import BaseModel
import datetime


class CreditCardUser(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str | datetime.date
    is_existing_customer: bool
    credit_card_number: str
    expiration_date: str | datetime.date
    cvv: str
    credit_card_issuer: str

    def parse_dates(self):
        self.date_of_birth = datetime.datetime.strptime(
            self.date_of_birth, "%Y-%m-%d"
        ).date()
        expiration_year, expiration_month = map(int, self.expiration_date.split("-"))
        self.expiration_date = datetime.date(expiration_year, expiration_month, 1)

    def create_credit_card_user(self):
        self.parse_dates()
        return self
