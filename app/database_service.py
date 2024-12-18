"""
This module contains the DataBaseService class, which is responsible for interacting with the
Supabase database. It contains methods for checking the credit score and duration of a user, as well
as recording the transaction of a credit approval request.

Classes:
    DataBaseService

Dependencies:
    - random: This module implements pseudo-random number generators for various distributions.
    - os: The OS module provides a way of using operating system dependent functionality.
    - init_db: The function to initialize the Supabase client.
    - CreditApprovalRequest: The class representing a credit approval request.
"""

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

    @staticmethod
    def fetch_credit_score_and_duration_from_db(
        credit_approval_request: CreditApprovalRequest,
    ) -> dict:
        """
        Fetch the credit score and credit duration of the user by querying the Supabase database.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The user to fetch the data for.

        Returns:
            dict: A dictionary containing the credit score and credit duration of the user.
        """
        db = init_db()
        data: dict = (
            db.table("credit_scores")
            .select("score, duration")
            .eq("card_number", credit_approval_request.credit_card_number)
            .execute()
        )
        result = {}

        try:
            credit_score = result["score"] = data.data[0]["score"]
        except IndexError:
            credit_score = result["score"] = random.randint(
                int(os.getenv("RANDOM_CREDIT_SCORE_MIN")),
                int(os.getenv("RANDOM_CREDIT_SCORE_MAX")),
            )

        try:
            credit_duration = result["duration"] = data.data[0]["duration"]
        except IndexError:
            credit_duration = result["duration"] = random.randint(
                int(os.getenv("RANDOM_CREDIT_DURATION_MIN")),
                int(os.getenv("RANDOM_CREDIT_DURATION_MAX")),
            )

        return credit_score, credit_duration

    @staticmethod
    def record_credit_approval_request_transaction(
        credit_approval_request: CreditApprovalRequest,
        errors: str = None,
        approval_status: str = False,
    ) -> None:
        """
        Record the transaction of the credit approval request in the Supabase database.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to record.
            errors (str): The errors that occurred during the credit approval request.
            approved (bool): Whether the credit was approved or denied.
        """
        db = init_db()
        if not approval_status or errors:
            approved = False
        else:
            approved = True
        (
            db.table("transactions")
            .insert(
                {
                    "card_number": credit_approval_request.credit_card_number,
                    "approved?": approved,
                    "errors": errors,
                }
            )
            .execute()
        )
