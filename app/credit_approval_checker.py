"""
This module contains the CreditApprovalChecker class which is responsible for checking if a user is
approved based on the credit approval criteria. The user is approved if they are an existing
customer, or if they are of legal age and their credit score and credit duration are within the
approval limits.

Classes:
    CreditApprovalChecker

Dependencies:
    - os: The OS module provides a way of using operating system dependent functionality.
    - datetime: The datetime module supplies classes for manipulating dates and times.
    - DataBaseService: The class to interact with the database.
    - CreditApprovalRequest: The class representing a credit approval request.
"""

import os
import datetime
from .database_methods import DataBaseService


class CreditApprovalChecker:
    """
    The CreditApprovalChecker class is responsible for checking if a user is approved based on the
    credit approval criteria. The user is approved if they are an existing customer, or if they are
    of legal age and their credit score and credit duration are within the approval limits.

    Methods:
        _check_if_creditee_is_of_legal_age_from_credit_approval_request(credit_approval_request):
            Check if the user is of legal age from the credit approval request.
        _check_if_credit_score_and_credit_duration_within_approval_limits(credit_approval_request):
            Checks if the credit score and credit duration are within the approval limits.
        check_credit_approval_request_result(credit_approval_request): Check if the user is approved
            based on the credit approval criteria.
    """

    @staticmethod
    def _check_if_creditee_is_of_legal_age_from_credit_approval_request(
        credit_approval_request,
    ) -> bool:
        """
        Check if the user is of legal age from the credit approval request.

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
    def _check_if_credit_score_and_credit_duration_within_approval_limits(
        credit_approval_request,
    ) -> bool:
        """
        Checks if the credit score and credit duration are within the approval limits.

        Parameters:
            credit_approval_request(CreditApprovalRequest): The request to check the credit score and
            duration for.

        Returns:
            bool: True if the user is approved, False otherwise.
        """
        credit_score = DataBaseService().check_credit_score_for_credit_approval_request(
            credit_approval_request
        )
        credit_duration = (
            DataBaseService().check_credit_duration_for_credit_approval_request(
                credit_approval_request
            )
        )

        credit_criteria = {
            "poor": {
                "range": (
                    int(os.getenv("POOR_CREDIT_MIN")),
                    int(os.getenv("POOR_CREDIT_MAX")),
                ),
                "min_duration": int(os.getenv("POOR_CREDIT_MIN_DURATION")),
            },
            "fair": {
                "range": (
                    int(os.getenv("FAIR_CREDIT_MIN")),
                    int(os.getenv("FAIR_CREDIT_MAX")),
                ),
                "min_duration": int(os.getenv("FAIR_CREDIT_MIN_DURATION")),
            },
            "good": {
                "range": (
                    int(os.getenv("GOOD_CREDIT_MIN")),
                    int(os.getenv("GOOD_CREDIT_MAX")),
                ),
                "min_duration": int(os.getenv("GOOD_CREDIT_MIN_DURATION")),
            },
            "very_good": {
                "range": (
                    int(os.getenv("VERY_GOOD_CREDIT_MIN")),
                    int(os.getenv("VERY_GOOD_CREDIT_MAX")),
                ),
                "min_duration": int(os.getenv("VERY_GOOD_CREDIT_MIN_DURATION")),
            },
            "excellent": {
                "range": (
                    int(os.getenv("EXCELLENT_CREDIT_MIN")),
                    int(os.getenv("EXCELLENT_CREDIT_MAX")),
                ),
                "min_duration": int(os.getenv("EXCELLENT_CREDIT_MIN_DURATION")),
            },
            "exceptional": {
                "range": (
                    int(os.getenv("EXCEPTIONAL_CREDIT_MIN")),
                    int(os.getenv("EXCEPTIONAL_CREDIT_MAX")),
                ),
                "min_duration": int(os.getenv("EXCEPTIONAL_CREDIT_MIN_DURATION")),
            },
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
        Check if the user is approved based on the credit approval criteria. The user is approved if
        they are an existing customer, or if they are of legal age and their credit score and credit
        duration are within the approval limits.

        Parameters:
            user (CreditApprovalRequest): The user to check the credit approval.

        Returns:
            bool: True if the user is approved, False otherwise.
        """
        if credit_approval_request.is_existing_customer:
            return True

        if CreditApprovalChecker._check_if_creditee_is_of_legal_age_from_credit_approval_request(
            credit_approval_request
        ) and CreditApprovalChecker._check_if_credit_score_and_credit_duration_within_approval_limits(
            credit_approval_request
        ):
            return True
        return False
