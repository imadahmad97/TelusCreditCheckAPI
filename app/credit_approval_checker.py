from .credit_card_validator import CreditCardValidator
import datetime
from . import init_app


class CreditApprovalChecker:
    def check_user_over_18(user):
        days_in_year = 365.2425
        age = (datetime.datetime.now().date() - user.date_of_birth).days / days_in_year
        if age < 18:
            return False
        return True

    def check_existing_customer(user):
        return user.is_existing_customer

    def check_credit_score(user):
        supabase = init_app()
        score = (
            supabase.table("credit_scores")
            .select("score")
            .eq("card_number", user.credit_card_number)
            .execute()
        )
        return score.data[0]["score"]

    def check_approval(user):
        print("ttest")
        print(CreditApprovalChecker.check_credit_score(user))
        if CreditApprovalChecker.check_existing_customer(user):
            return True

        elif (
            CreditApprovalChecker.check_user_over_18(user)
            and CreditApprovalChecker.check_credit_score(user) >= 700
        ):
            return True
        return False
