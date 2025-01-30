"""
This module contains the DataBaseService class, which is responsible for interacting with the
Supabase database. It contains methods for checking the credit score and duration of a user, as well
as recording the transaction of a credit approval request.

Classes:
    DataBaseService

Dependencies:
    - random: This module implements pseudo-random number generators for various distributions.
    - os: This module provides a portable way of using operating system-dependent functionality.
    - Any: A special type that indicates an unconstrained type.
    - create_client: A function that creates a Supabase client object.
    - Client: The Supabase client object for interacting with the database.
"""

import random
import os
import logging
from typing import Any
from supabase import create_client, Client


class DataBaseService:
    """
    This class is responsible for interacting with the Supabase database. It contains methods for
    checking the credit score and duration of a user, as well as recording the transaction of a
    credit approval request.

    Attributes:
        supabase (Client): The Supabase client object for interacting with the

    Methods:
        fetch_credit_score_and_duration_from_db: Fetch the credit score and credit duration of the
        user by querying the Supabase database.
        record_credit_approval_request_transaction: Record the transaction of the credit approval
        request in the Supabase database.
    """

    def __init__(self, url: str, key: str) -> None:
        """
        Initialize the Supabase client's PostgreSQL database for the application.
        """
        self.supabase: Client = create_client(url, key)
        self._test_db_connection()

    def _test_db_connection(self) -> None:
        """Attempt a simple query to confirm that the Supabase DB is reachable. Raises
        ConnectionError if not.
        """
        try:
            self.supabase.table("transactions").select("*").limit(1).execute()
        except Exception as e:
            raise ConnectionError from e

    def fetch_credit_score_and_duration_from_db(self, credit_card_number) -> tuple:
        """
        Fetch the credit score and credit duration of the user by querying the Supabase database.

        Parameters:
            credit_card_number (str): The credit card number of the user.

        Returns:
            tuple: A tuple containing the credit score and credit duration of the user.
        """

        result = {}

        try:
            data: Any = (
                self.supabase.table("credit_scores")
                .select("score, duration")
                .eq("card_number", credit_card_number)
                .execute()
            )

            credit_score = result["score"] = data.data[0]["score"]
            credit_duration = result["duration"] = data.data[0]["duration"]

        except Exception:
            logging.error(
                "Failed to fetch credit score and/or duration, using random values"
            )
            credit_score = result["score"] = random.randint(
                int(os.getenv("RANDOM_CREDIT_SCORE_MIN", "300")),
                int(os.getenv("RANDOM_CREDIT_SCORE_MAX", "850")),
            )
            credit_duration = result["duration"] = random.randint(
                int(os.getenv("RANDOM_CREDIT_DURATION_MIN", "0")),
                int(os.getenv("RANDOM_CREDIT_DURATION_MAX", "10")),
            )

        return credit_score, credit_duration

    def record_credit_approval_request_transaction(
        self,
        credit_card_number: str,
        is_approved: bool,
        errors: str,
    ) -> None:
        """
        Record the transaction of the credit approval request in the Supabase database.

        Parameters:
            credit_card_number (str): The credit card number of the user.
            is_approved (bool): A boolean indicating if the credit approval request was approved.
            errors (str): A string containing the errors encountered during the credit approval
            request.
        """
        try:
            (
                self.supabase.table("transactions")
                .insert(
                    {
                        "card_number": credit_card_number,
                        "approved?": is_approved,
                        "errors": errors,
                    }
                )
                .execute()
            )
        except Exception as e:
            logging.error("Failed to record transaction: %s", e)
