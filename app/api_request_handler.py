from .credit_card_validator import CreditCardValidator
from .credit_card_user import CreditCardUser
from .credit_approval_checker import CreditApprovalChecker


def handle_credit_check_request(user: CreditCardUser):
    CreditCardUser.create_credit_card_user(user)
    CreditCardValidator.validate(user)
    if CreditApprovalChecker.check_approval(user):
        return {"credit_approval": "approved"}
    return {"credit_approval": "denied"}
