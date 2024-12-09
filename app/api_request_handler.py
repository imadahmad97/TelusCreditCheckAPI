from .credit_card_validator import CreditCardValidator
from .credit_card_user import CreditCardUser


def handle_credit_check_request(user: CreditCardUser):
    CreditCardUser.create_credit_card_user(user)
    CreditCardValidator.validate(user)
    return {"credit_check": "success"}
