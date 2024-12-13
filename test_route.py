"""
This module contains a test suite for the /check_credit route in the main.py module. 

The test suite includes the following test cases:
    - Test credit check for a valid user
    - Test credit check route with missing fields
    - Test credit check route with an invalid card number length
    - Test credit check route with an invalid CVV length
    - Test credit check route with an invalid card number
    - Test credit check for an existing customer
    - Test credit check for a user with a credit score of 800
    - Test credit check for a user under 18 years old who is not an existing customer
    - Test credit check for a user under 18 years old who is an existing customer
    - Test credit check for a user with a credit score of 350 and a credit history duration of 10 years
    - Test credit check for a user with a credit score of 350 and a credit history duration of 9 years
    - Test credit check for a user with a credit score of 550 and a credit history duration of 7 years
    - Test credit check for a user with a credit score of 550 and a credit history duration of 6 years
    - Test credit check for a user with a credit score of 650 and a credit history duration of 5 years
    - Test credit check for a user with a credit score of 650 and a credit history duration of 4 years
    - Test credit check for a user with a credit score of 725 and a credit history duration of 3 years
    - Test credit check for a user with a credit score of 725 and a credit history duration of 2 years
    - Test credit check for a user with a credit score of 775 and a credit history duration of 1 year
    - Test credit check for a user with a credit score of 775 and no credit history

The test suite can be run by executing the following command:
    - python test_route.py

Dependencies:
    - pytest
    - fastapi
    - main
    - TestClient
"""

import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

base_data = {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "2000-01-01",
    "is_existing_customer": False,
    "credit_card_number": "4929439557473282537",
    "expiration_date": "2027-08",
    "cvv": "123",
    "credit_card_issuer": "Visa",
}


def test_credit_check_for_route_valid_user():
    """
    Test case to check if the credit check route returns the expected response for a valid user.

    Asserts:
        - The status code of the response is 200
        - The response is an approval
    """
    response = client.post("/check_credit", data=base_data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_credit_check_route_missing_fields():
    """
    Test case to check if the credit check route returns the expected response when required fields
    are missing.

    Asserts:
        - The status code of the response is 422
    """
    data = base_data.copy()
    del data["credit_card_issuer"]
    response = client.post("/check_credit", data=data)
    assert response.status_code == 422


def test_credit_check_route_invalid_card_number_length():
    """
    Test case to check if the credit check route returns the expected response when an invalid card
    number is provided.

    Asserts:
        - The status code of the response is 400
        - The response is as expected
    """
    data = base_data.copy()
    data["credit_card_number"] = "12345678901234565891"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "400: Card number must be between 8 and 19 digits; 400: Invalid credit card number; ",
    }


def test_credit_check_route_invalid_cvv_length():
    data = base_data.copy()
    data["cvv"] = "12345"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "400: CVV must be 3 or 4 digits; ",
    }


def test_credit_check_route_invalid_card_number():
    data = base_data.copy()
    data["credit_card_number"] = "1234567890123456"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "400: Invalid credit card number; ",
    }


def test_existing_customer_always_approved():
    """
    Test case to check if the credit check route returns the expected response for an existing
    customer.

    Asserts:
        - The status code of the response is 200
        - The response is an approval
    """
    data = base_data.copy()
    data["is_existing_customer"] = True
    data["credit_card_number"] = "373337942404166"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_800_always_approved():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 800.

    Asserts:
        - The status code of the response is 200
        - The response is an approval
    """
    data = base_data.copy()
    data["credit_card_number"] = "5127626881039365"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_under_18_denied_when_not_existing_customer():
    """
    Test case to check if the credit check route returns the expected response for a user under 18
    years old who is not an existing customer.

    Asserts:
        - The status code of the response is 200
        - The response is a denial
    """
    data = base_data.copy()
    data["date_of_birth"] = "2010-01-01"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


def test_under_18_approved_when_existing_customer():
    """
    Test case to check if the credit check route returns the expected response for a user under 18
    years old who is an existing customer.

    Asserts:
        - The status code of the response is 200
        - The response is an approval
    """
    data = base_data.copy()
    data["date_of_birth"] = "2010-01-01"
    data["is_existing_customer"] = True
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_350_duration_10():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 350 and a credit history duration of 10 years.

    Asserts:
        - The status code of the response is 200
        - The response is an approval
    """
    data = base_data.copy()
    data["credit_card_number"] = "4929439557473282537"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_350_duration_9():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 350 and a credit history duration of 9 years.

    Asserts:
        - The status code of the response is 200
        - The response is a denial
    """
    data = base_data.copy()
    data["credit_card_number"] = "373337942404166"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


def test_score_550_duration_7():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 550 and a credit history duration of 7 years.

    Asserts:
        - The status code of the response is 200
        - The response is an approval
    """
    data = base_data.copy()
    data["credit_card_number"] = "349577280889988"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_550_duration_6():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 550 and a credit history duration of 6 years.

    Asserts:
        - The status code of the response is 200
        - The response is a denial
    """
    data = base_data.copy()
    data["credit_card_number"] = "379765683272919"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


def test_score_650_duration_5():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 650 and a credit history duration of 5 years.

    Asserts:
        - The status code of the response is 200
        - The response is an approval
    """
    data = base_data.copy()
    data["credit_card_number"] = "6011693232839786565"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_650_duration_4():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 650 and a credit history duration of 4 years.

    Asserts:
        - The status code of the response is 200
        - The response is a denial
    """
    data = base_data.copy()
    data["credit_card_number"] = "6011775597776401"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


def test_score_725_duration_3():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 725 and a credit history duration of 3 years.

    Asserts:
        - The status code of the response is 200
        - The response is an approval
    """
    data = base_data.copy()
    data["credit_card_number"] = "4916159168643657"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_725_duration_2():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 725 and a credit history duration of 2 years.

    Asserts:
        - The status code of the response is 200
        - The response is a denial
    """
    data = base_data.copy()
    data["credit_card_number"] = "4058617700662392"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


def test_score_775_duration_1():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 775 and a credit history duration of 1 year.

    Asserts:
        - The status code of the response is 200
        - The response is an approval
    """
    data = base_data.copy()
    data["credit_card_number"] = "5510642096381885"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_775_duration_0():
    """
    Test case to check if the credit check route returns the expected response for a user with a
    credit score of 775 and no credit history.

    Asserts:
        - The status code of the response is 200
        - The response is a denial
    """
    data = base_data.copy()
    data["credit_card_number"] = "2221005919057420"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


if __name__ == "__main__":
    pytest.main()
