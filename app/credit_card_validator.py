import datetime
from fastapi import HTTPException
from .credit_card_user import CreditCardUser


class CreditCardValidator:
    @staticmethod
    def validate_number_lengths(credit_card_user: CreditCardUser):
        if len(credit_card_user.credit_card_number) != 16:
            raise HTTPException(status_code=400, detail="Card number must be 16 digits")
        if not 3 <= len(credit_card_user.cvv) <= 4:
            raise HTTPException(status_code=400, detail="CVV must be 3 or 4 digits")

    @staticmethod
    def validate_expiration_date(credit_card_user: CreditCardUser):
        if credit_card_user.expiration_date < datetime.date.today():
            raise HTTPException(status_code=400, detail="Card is expired")

    @staticmethod
    def validate_credit_card_issuer(credit_card_user: CreditCardUser):
        if credit_card_user.credit_card_issuer.lower() not in [
            "visa",
            "mastercard",
            "american express",
        ]:
            raise HTTPException(status_code=400, detail="Invalid credit card issuer")

    @staticmethod
    def validate(credit_card_user: CreditCardUser):
        CreditCardValidator.validate_number_lengths(credit_card_user)
        CreditCardValidator.validate_expiration_date(credit_card_user)
        CreditCardValidator.validate_credit_card_issuer(credit_card_user)
        return True
