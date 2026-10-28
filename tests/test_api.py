
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app, Base, get_db


# Use a separate in-memory database for every test.
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def get_auth_headers(client, email="test@example.com"):
    """Register and log in a test user, then return auth headers."""
    password = "TestPassword123!"

    registration = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert registration.status_code == 201

    login = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login.status_code == 200

    token = login.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def create_sample_expense(client, headers):
    return client.post(
        "/expenses",
        headers=headers,
        json={
            "amount": 150,
            "category": "Food",
            "description": "Lunch",
            "expense_date": "2026-10-25",
        },
    )


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_create_expense(client):
    headers = get_auth_headers(client)
    response = create_sample_expense(client, headers)

    assert response.status_code == 201
    assert response.json()["amount"] == 150
    assert response.json()["category"] == "Food"


def test_list_expenses(client):
    headers = get_auth_headers(client)
    create_sample_expense(client, headers)

    response = client.get("/expenses", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["description"] == "Lunch"


def test_filter_by_category(client):
    headers = get_auth_headers(client)
    create_sample_expense(client, headers)

    client.post(
        "/expenses",
        headers=headers,
        json={
            "amount": 80,
            "category": "Transport",
            "description": "Bus ticket",
            "expense_date": "2026-10-26",
        },
    )

    response = client.get(
        "/expenses?category=Food",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "Food"


def test_get_missing_expense(client):
    headers = get_auth_headers(client)

    response = client.get("/expenses/99999", headers=headers)

    assert response.status_code == 404


def test_reject_negative_amount(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/expenses",
        headers=headers,
        json={
            "amount": -50,
            "category": "Food",
            "description": "Invalid expense",
        },
    )

    assert response.status_code == 422


def test_update_expense(client):
    headers = get_auth_headers(client)
    created = create_sample_expense(client, headers)
    assert created.status_code == 201

    expense_id = created.json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        headers=headers,
        json={
            "amount": 200,
            "category": "Shopping",
            "description": "New shirt",
            "expense_date": "2026-10-27",
        },
    )

    assert response.status_code == 200
    assert response.json()["amount"] == 200
    assert response.json()["category"] == "Shopping"


def test_delete_expense(client):
    headers = get_auth_headers(client)
    created = create_sample_expense(client, headers)
    expense_id = created.json()["id"]

    response = client.delete(
        f"/expenses/{expense_id}",
        headers=headers,
    )

    assert response.status_code == 200

    missing = client.get(
        f"/expenses/{expense_id}",
        headers=headers,
    )
    assert missing.status_code == 404


def test_summary(client):
    headers = get_auth_headers(client)
    create_sample_expense(client, headers)

    response = client.get("/summary", headers=headers)

    assert response.status_code == 200
    assert response.json()["total_spending"] == 150
    assert response.json()["number_of_expenses"] == 1


def test_expenses_require_authentication(client):
    response = client.get("/expenses")

    assert response.status_code == 401


def test_users_cannot_see_each_others_expenses(client):
    headers_a = get_auth_headers(client, "usera@example.com")
    headers_b = get_auth_headers(client, "userb@example.com")

    created = create_sample_expense(client, headers_a)
    assert created.status_code == 201

    # User B should see an empty list.
    response = client.get("/expenses", headers=headers_b)
    assert response.status_code == 200
    assert response.json() == []

    expense_id = created.json()["id"]

    # User B cannot access, update, or delete User A's expense.
    get_response = client.get(
        f"/expenses/{expense_id}",
        headers=headers_b,
    )
    assert get_response.status_code == 404

    update_response = client.put(
        f"/expenses/{expense_id}",
        headers=headers_b,
        json={
            "amount": 500,
            "category": "Other",
            "description": "Unauthorized update",
            "expense_date": "2026-10-27",
        },
    )
    assert update_response.status_code == 404

    delete_response = client.delete(
        f"/expenses/{expense_id}",
        headers=headers_b,
    )
    assert delete_response.status_code == 404


def test_summary_only_includes_current_users_expenses(client):
    headers_a = get_auth_headers(client, "usera@example.com")
    headers_b = get_auth_headers(client, "userb@example.com")

    create_sample_expense(client, headers_a)

    response = client.get("/summary", headers=headers_b)

    assert response.status_code == 200
    assert response.json()["total_spending"] == 0
    assert response.json()["number_of_expenses"] == 0
