import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

base_data = {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "2000-01-01",
    "is_existing_customer": False,
    "credit_card_number": "1111222233334444",
    "expiration_date": "2027-08",
    "cvv": "123",
    "credit_card_issuer": "Visa",
}


def test_credit_check_for_route_valid_user():
    response = client.post("/check_credit", data=base_data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_credit_check_route_missing_fields():
    data = base_data.copy()
    del data["credit_card_issuer"]
    response = client.post("/check_credit", data=data)
    assert response.status_code == 422


def test_credit_check_route_invalid_card_number():
    data = base_data.copy()
    data["credit_card_number"] = "12345678901234565"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Card number must be 16 digits",
    }


def test_existing_customer_always_approved():
    data = base_data.copy()
    data["is_existing_customer"] = True
    data["credit_card_number"] = "1111222233334444"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_800_always_approved():
    data = base_data.copy()
    data["credit_card_number"] = "1234567891234567"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_under_18_denied_when_not_existing_customer():
    data = base_data.copy()
    data["date_of_birth"] = "2010-01-01"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


def test_under_18_approved_when_existing_customer():
    data = base_data.copy()
    data["date_of_birth"] = "2010-01-01"
    data["is_existing_customer"] = True
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_350_duration_10():
    data = base_data.copy()
    data["credit_card_number"] = "0637427684924651"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_350_duration_9():
    data = base_data.copy()
    data["credit_card_number"] = "8938533129388817"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


def test_score_550_duration_7():
    data = base_data.copy()
    data["credit_card_number"] = "6006744823964515"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_550_duration_6():
    data = base_data.copy()
    data["credit_card_number"] = "3821114600535667"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


def test_score_650_duration_5():
    data = base_data.copy()
    data["credit_card_number"] = "8044471595464609"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_650_duration_4():
    data = base_data.copy()
    data["credit_card_number"] = "8009978420510579"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


def test_score_725_duration_3():
    data = base_data.copy()
    data["credit_card_number"] = "0047057200562728"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_725_duration_2():
    data = base_data.copy()
    data["credit_card_number"] = "0118448060070548"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


def test_score_775_duration_1():
    data = base_data.copy()
    data["credit_card_number"] = "1234567891234567"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "approved"}


def test_score_775_duration_0():
    data = base_data.copy()
    data["credit_card_number"] = "2468123456789999"
    response = client.post("/check_credit", data=data)
    assert response.status_code == 200
    assert response.json() == {"credit_approval": "denied"}


if __name__ == "__main__":
    pytest.main()
