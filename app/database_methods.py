import random
import os
from . import init_db
from .credit_approval_request import CreditApprovalRequest


class DataBaseService:
    """
    This class is responsible for interacting with the Supabase database. It contains methods for
    checking the credit score and duration of a user, as well as recording the transaction of a
    credit approval request.

    Attributes:
        db (SupabaseClient): The Supabase client used to interact with the database

    Methods:
        check_credit_score_for_credit_approval_request: Check the credit score of the user by
        querying the Supabase database.
        check_credit_duration_for_credit_approval_request: Check the credit duration that the user
        has had credit by querying the Supabase database.
        record_credit_approval_request_transaction: Record the transaction of the credit approval
        request in the Supabase database.
    """

    def __init__(self):
        self.db = init_db()

    def check_credit_score_for_credit_approval_request(
        self, credit_approval_request: CreditApprovalRequest
    ) -> int:
        """
        Check the credit score of the user by querying the Supabase database.

        Parameters:
            user (CreditApprovalRequest): The user to check the credit score for.

        Returns:
            int: The credit score of the user.
        """
        score = (
            self.db.table("credit_scores")
            .select("score")
            .eq("card_number", credit_approval_request.credit_card_number)
            .execute()
        )
        try:
            return score.data[0]["score"]
        except IndexError:
            return random.randint(
                int(os.getenv("RANDOM_CREDIT_SCORE_MIN")),
                int(os.getenv("RANDOM_CREDIT_SCORE_MAX")),
            )

    def check_credit_duration_for_credit_approval_request(
        self,
        credit_approval_request: CreditApprovalRequest,
    ) -> int:
        """
        Check the credit duration that the user has had credit by querying the Supabase database.

        Parameters:
            user (CreditApprovalRequest): The user to check the credit duration for.

        Returns:
            float: The credit duration of the user (years).
        """
        duration = (
            self.db.table("credit_scores")
            .select("duration")
            .eq("card_number", credit_approval_request.credit_card_number)
            .execute()
        )
        try:
            return duration.data[0]["duration"]
        except IndexError:
            return random.randint(
                int(os.getenv("RANDOM_CREDIT_DURATION_MIN")),
                int(os.getenv("RANDOM_CREDIT_DURATION_MAX")),
            )

    def record_credit_approval_request_transaction(
        self,
        credit_approval_request: CreditApprovalRequest,
        errors: str = None,
        approved: bool = False,
    ) -> None:
        """
        Record the transaction of the credit approval request in the Supabase database.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to record.
            errors (str): The errors that occurred during the credit approval request.
            approved (bool): Whether the credit was approved or denied.
        """
        (
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
