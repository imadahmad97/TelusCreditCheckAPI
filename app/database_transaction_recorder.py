from . import init_db
from .credit_approval_request import CreditApprovalRequest


class DatabaseTransactionRecorder:
    def __init__(self):
        self.db = init_db()

    def record_transaction(
        self,
        credit_approval_request: CreditApprovalRequest,
        errors: str = None,
        approved: bool = False,
    ):
        response = (
            self.db.table("transactions")
            .insert(
                {
                    "card_number": credit_approval_request.credit_card_number,
                    "approved?": approved,
                    "errors": errors,
                }
            )
            .execute()
        )
