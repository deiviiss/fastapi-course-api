"""

"""

from fastapi import status


def test_create_customer(client):
    """
    Test for the client
    """
    response = client.post(
        "/customers",
        json={
            "name": "John Doe",
            "email": "jhon@example.com",
            "age": 30,
        }
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_read_customer(client):
    """
    Test for the client
    """
    response = client.post(
        "/customers",
        json={
            "name": "John Doe",
            "email": "jhon@example.com",
            "age": 30,
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json()["id"]
    response_read = client.get(f"/customers/{customer_id}")

    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["id"] == customer_id
    assert response_read.json()["name"] == "John Doe"
    assert response_read.json()["email"] == "jhon@example.com"
    assert response_read.json()["age"] == 30
