import datetime


class CreditApprovalResponse:
    def __init__(
        self,
        is_existing_customer: bool,
        date_of_birth: datetime.date,
        is_approved: bool,
        errors: str = "",
        response: str = "",
        credit_card_number: str = "",
    ):
        self.is_existing_customer = is_existing_customer
        self.date_of_birth = date_of_birth
        self.is_approved = is_approved
        self.errors = errors
        self.response = response
        self.credit_card_number = credit_card_number
