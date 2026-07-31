from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)



def test_create_expense():

    response = client.post(
        "/expenses",
        json={
            "id":1,
            "title":"Coffee",
            "amount":100,
            "category":"Food",
            "date":"2026-07-31"
        }
    )


    assert response.status_code == 200



def test_get_expenses():

    response = client.get(
        "/expenses"
    )

    assert response.status_code == 200



def test_category_filter():

    response = client.get(
        "/expenses?category=Food"
    )

    assert response.status_code == 200



def test_summary():

    response = client.get(
        "/expenses/summary"
    )

    assert response.status_code == 200



def test_delete():

    response = client.delete(
        "/expenses/1"
    )

    assert response.status_code == 200