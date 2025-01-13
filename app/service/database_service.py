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
from app.model.credit_approval_request import CreditApprovalRequest
from app.model.credit_approval_response import CreditApprovalResponse
from supabase import create_client, Client
from typing import Any


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

    def __init__(self, url, key):
        """
        Initialize the Supabase client's PostgreSQL database for the application.

        Returns:
            Client: The Supabase client
        """
        self.supabase: Client = create_client(url, key)

    def fetch_credit_score_and_duration_from_db(
        self,
        credit_approval_request: CreditApprovalRequest,
    ) -> tuple:
        """
        Fetch the credit score and credit duration of the user by querying the Supabase database.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The user to fetch the data for.

        Returns:
            dict: A dictionary containing the credit score and credit duration of the user.
        """
        db = self.supabase
        data: Any = (
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
                int(os.getenv("RANDOM_CREDIT_SCORE_MIN", "300")),
                int(os.getenv("RANDOM_CREDIT_SCORE_MAX", "850")),
            )

        try:
            credit_duration = result["duration"] = data.data[0]["duration"]
        except IndexError:
            credit_duration = result["duration"] = random.randint(
                int(os.getenv("RANDOM_CREDIT_DURATION_MIN", "0")),
                int(os.getenv("RANDOM_CREDIT_DURATION_MAX", "10")),
            )

        return credit_score, credit_duration

    def record_credit_approval_request_transaction(
        self,
        credit_approval_response: CreditApprovalResponse,
    ) -> None:
        """
        Record the transaction of the credit approval request in the Supabase database.

        Parameters:
            credit_approval_request (CreditApprovalRequest): The credit approval request to record.
            errors (str): The errors that occurred during the credit approval request.
            approved (bool): Whether the credit was approved or denied.
        """
        db = self.supabase
        (
            db.table("transactions")
            .insert(
                {
                    "card_number": credit_approval_response.credit_card_number,
                    "approved?": credit_approval_response.is_approved,
                    "errors": credit_approval_response.errors,
                }
            )
            .execute()
        )
