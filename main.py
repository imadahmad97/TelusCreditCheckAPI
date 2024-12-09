from fastapi import FastAPI, Form
from typing import Annotated
from app.creditcarduser import CreditCardUser

app = FastAPI()


@app.get("/check_credit")
async def root(user: Annotated[CreditCardUser, Form()]):
    return user.create_credit_card_user()
