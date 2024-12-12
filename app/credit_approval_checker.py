"""
A module to validate credit card information. It contains the CreditCardValidator class with methods
to validate the credit card number, expiration date, and issuer.

Classes:
    CreditCardValidator: A class to validate credit card information.
    
Dependencies:
    - datetime
    - HTTPException
    - CreditApprovalRequest
"""

import os
import datetime
from . import init_db


class CreditApprovalChecker:
    """
    A class to check the credit approval of a user. It contains methods to check if the user is over
    18, an existing customer, the credit score, and if the user is approved.

    Methods:
        check_if_user_over_18(user: CreditApprovalRequest) -> bool: Check if the user is over 18 years old.
        check_user_credit_score(user: CreditApprovalRequest) -> int: Check the credit score of the user.
        check_user_credit_duration(user: CreditApprovalRequest) -> int: Check the credit duration of the
        user.
        compare_score_and_duration(user_id: int) -> bool: Compare the credit score and duration of
        the user to the credit approval criteria.
        check_if_user_approved(user: CreditApprovalRequest) -> bool: Check if the user is approved.
    """

    @staticmethod
    def _check_if_creditee_is_at_least_18_years_old_from_credit_approval_request(
        credit_approval_request,
    ) -> bool:
        """
        Check if the user is over 18 years old.

        Parameters:
            credit_approval_request(CreditApprovalRequest): The user to check the age.

        Returns:
            bool: True if the user is over 18, False otherwise.
        """
        age = (
            datetime.datetime.now().date() - credit_approval_request.date_of_birth
        ).days / float(os.getenv("DAYS_IN_YEAR"))
        if age < int(os.getenv("LEGAL_AGE")):
            return False
        return True

    @staticmethod
    def _check_credit_score_for_credit_approval_request(credit_approval_request) -> int:
        """
        Check the credit score of the user by querying the Supabase database.

        Parameters:
            user (CreditApprovalRequest): The user to check the credit score for.

        Returns:
            int: The credit score of the user.
        """
        supabase = init_db()
        score = (
            supabase.table("credit_scores")
            .select("score")
            .eq("card_number", credit_approval_request.credit_card_number)
            .execute()
        )
        return score.data[0]["score"]

    @staticmethod
    def _check_credit_duration_for_credit_approval_request(
        credit_approval_request,
    ) -> int:
        """
        Check the credit duration that the user has had credit by querying the Supabase database.

        Parameters:
            user (CreditApprovalRequest): The user to check the credit duration for.

        Returns:
            float: The credit duration of the user (years).
        """
        supabase = init_db()
        duration = (
            supabase.table("credit_scores")
            .select("duration")
            .eq("card_number", credit_approval_request.credit_card_number)
            .execute()
        )
        return duration.data[0]["duration"]

    @staticmethod
    def _check_if_credit_score_and_credit_duration_within_approval_limits(user_id):
        """
        Compare the credit score and duration of the user to the credit approval criteria.

        Parameters:
            user_id (int): The user ID to check the credit score and duration.

        Returns:
            bool: True if the user is approved, False otherwise.
        """
        credit_score = (
            CreditApprovalChecker._check_credit_score_for_credit_approval_request(
                user_id
            )
        )
        credit_duration = (
            CreditApprovalChecker._check_credit_duration_for_credit_approval_request(
                user_id
            )
        )

        credit_criteria = {
            "poor": {"range": (300, 499), "min_duration": 10},
            "fair": {"range": (500, 599), "min_duration": 7},
            "good": {"range": (600, 699), "min_duration": 5},
            "very_good": {"range": (700, 749), "min_duration": 3},
            "excellent": {"range": (750, 799), "min_duration": 1},
            "exceptional": {"range": (800, 850), "min_duration": 0},
        }

        for criteria in credit_criteria.values():
            score_min, score_max = criteria["range"]
            if (
                score_min <= credit_score <= score_max
                and credit_duration >= criteria["min_duration"]
            ):
                return True

        return False

    @staticmethod
    def check_credit_approval_request_result(credit_approval_request) -> bool:
        """
        Check if the user is approved based on the credit approval criteria.

        Parameters:
            user (CreditApprovalRequest): The user to check the credit approval.

        Returns:
            bool: True if the user is approved, False otherwise.
        """
        if credit_approval_request.is_existing_customer:
            return True

        if CreditApprovalChecker._check_if_creditee_is_at_least_18_years_old_from_credit_approval_request(
            credit_approval_request
        ) and CreditApprovalChecker._check_if_credit_score_and_credit_duration_within_approval_limits(
            credit_approval_request
        ):
            return True
        return False
