from fastapi import FastAPI, Form
from typing import Annotated
from app.credit_card_user import CreditCardUser
from app.api_request_handler import handle_credit_check_request
from app import init_app

app = FastAPI()


@app.get("/check_credit")
async def root(user: Annotated[CreditCardUser, Form()]):
    return handle_credit_check_request(user)
