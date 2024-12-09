from fastapi import FastAPI
from pydantic import BaseModel
import datetime


class CreditCardUser(BaseModel):
    first_name: str
    last_name: str
    # date_of_birth: datetime.date
    is_existing_customer: bool
    credit_card_number: str
    # expiration_date: str
    cvv: str
    credit_card_issuer: str

    def create_credit_card_user(self):
        print(f"User: {self.first_name} {self.last_name}")
        return self
