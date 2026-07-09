import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.base import Base
from app.api.dependencies import get_db
import app.models as models

# ─── Test Database Setup ──────────────────────────────────────────

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Create test user
    from app.core.security import get_password_hash
    user = models.User(username="testadmin", hashed_password=get_password_hash("testpass"), role="admin")
    db.add(user)
    db.commit()
    
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(setup_database):
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def auth_client(client):
    # Log in to get the token
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "testadmin", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = response.json()["access_token"]
    
    # Create an authenticated client
    with TestClient(app) as auth_c:
        auth_c.headers.update({"Authorization": f"Bearer {token}"})
        yield auth_c

# ─── Test Data ────────────────────────────────────────────────

VALID_TICKET = {
    "title": "Test Ticket",
    "description": "This is a test description that meets minimum length",
    "customerName": "John Doe",
    "customerEmail": "john@example.com",
    "priority": "High"
}

# ─── Auth Tests ───────────────────────────────────────────────

def test_unauthorized_access():
    unauth_client = TestClient(app)
    response = unauth_client.get("/api/v1/tickets/")
    assert response.status_code == 401

# ─── Happy Path ───────────────────────────────────────────────

def test_create_ticket_success(auth_client):
    response = auth_client.post("/api/v1/tickets/", json=VALID_TICKET)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Ticket"
    assert data["status"] == "Open"
    assert data["priority"] == "High"
    assert "id" in data
    assert "createdAt" in data


def test_get_tickets(auth_client):
    auth_client.post("/api/v1/tickets/", json=VALID_TICKET)
    response = auth_client.get("/api/v1/tickets/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_ticket_by_id(auth_client):
    create = auth_client.post("/api/v1/tickets/", json=VALID_TICKET)
    ticket_id = create.json()["id"]
    response = auth_client.get(f"/api/v1/tickets/{ticket_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ticket_id


def test_update_ticket_status(auth_client):
    create = auth_client.post("/api/v1/tickets/", json=VALID_TICKET)
    ticket_id = create.json()["id"]
    update = auth_client.patch(f"/api/v1/tickets/{ticket_id}", json={"status": "In Progress"})
    assert update.status_code == 200
    assert update.json()["status"] == "In Progress"


def test_update_ticket_priority(auth_client):
    create = auth_client.post("/api/v1/tickets/", json=VALID_TICKET)
    ticket_id = create.json()["id"]
    update = auth_client.patch(f"/api/v1/tickets/{ticket_id}", json={"priority": "Low"})
    assert update.status_code == 200
    assert update.json()["priority"] == "Low"


def test_filter_tickets_by_status(auth_client):
    auth_client.post("/api/v1/tickets/", json=VALID_TICKET)
    response = auth_client.get("/api/v1/tickets/?status=Open")
    assert response.status_code == 200
    for ticket in response.json():
        assert ticket["status"] == "Open"


def test_filter_tickets_by_priority(auth_client):
    auth_client.post("/api/v1/tickets/", json=VALID_TICKET)
    response = auth_client.get("/api/v1/tickets/?priority=High")
    assert response.status_code == 200
    for ticket in response.json():
        assert ticket["priority"] == "High"


# ─── Input Validation: Missing Required Fields ──────────────

def test_create_ticket_missing_title(auth_client):
    data = {**VALID_TICKET}
    del data["title"]
    response = auth_client.post("/api/v1/tickets/", json=data)
    assert response.status_code == 422


def test_create_ticket_missing_description(auth_client):
    data = {**VALID_TICKET}
    del data["description"]
    response = auth_client.post("/api/v1/tickets/", json=data)
    assert response.status_code == 422


def test_create_ticket_missing_customerName(auth_client):
    data = {**VALID_TICKET}
    del data["customerName"]
    response = auth_client.post("/api/v1/tickets/", json=data)
    assert response.status_code == 422


def test_create_ticket_missing_customerEmail(auth_client):
    data = {**VALID_TICKET}
    del data["customerEmail"]
    response = auth_client.post("/api/v1/tickets/", json=data)
    assert response.status_code == 422


def test_create_ticket_missing_priority(auth_client):
    data = {**VALID_TICKET}
    del data["priority"]
    response = auth_client.post("/api/v1/tickets/", json=data)
    assert response.status_code == 422


# ─── Input Validation: Invalid Values ────────────────────────

def test_create_ticket_invalid_email(auth_client):
    response = auth_client.post("/api/v1/tickets/", json={**VALID_TICKET, "customerEmail": "not-an-email"})
    assert response.status_code == 422


def test_create_ticket_invalid_priority(auth_client):
    response = auth_client.post("/api/v1/tickets/", json={**VALID_TICKET, "priority": "Urgent"})
    assert response.status_code == 422


def test_create_ticket_empty_title(auth_client):
    response = auth_client.post("/api/v1/tickets/", json={**VALID_TICKET, "title": ""})
    assert response.status_code == 422


def test_create_ticket_whitespace_only_title(auth_client):
    response = auth_client.post("/api/v1/tickets/", json={**VALID_TICKET, "title": "   "})
    assert response.status_code == 422


def test_create_ticket_whitespace_only_description(auth_client):
    response = auth_client.post("/api/v1/tickets/", json={**VALID_TICKET, "description": "   "})
    assert response.status_code == 422


def test_create_ticket_whitespace_only_customerName(auth_client):
    response = auth_client.post("/api/v1/tickets/", json={**VALID_TICKET, "customerName": "   "})
    assert response.status_code == 422


def test_create_ticket_title_too_long(auth_client):
    response = auth_client.post("/api/v1/tickets/", json={**VALID_TICKET, "title": "A" * 201})
    assert response.status_code == 422


def test_create_ticket_strips_whitespace(auth_client):
    """Valid input with leading/trailing whitespace should be accepted and stripped."""
    response = auth_client.post("/api/v1/tickets/", json={**VALID_TICKET, "title": "  Padded Title  "})
    assert response.status_code == 201
    assert response.json()["title"] == "Padded Title"


# ─── Update Validation ───────────────────────────────────────

def test_update_ticket_invalid_status(auth_client):
    create = auth_client.post("/api/v1/tickets/", json=VALID_TICKET)
    ticket_id = create.json()["id"]
    response = auth_client.patch(f"/api/v1/tickets/{ticket_id}", json={"status": "Closed"})
    assert response.status_code == 422


def test_update_ticket_empty_body(auth_client):
    create = auth_client.post("/api/v1/tickets/", json=VALID_TICKET)
    ticket_id = create.json()["id"]
    response = auth_client.patch(f"/api/v1/tickets/{ticket_id}", json={})
    assert response.status_code == 422


def test_update_nonexistent_ticket(auth_client):
    response = auth_client.patch("/api/v1/tickets/99999", json={"status": "Resolved"})
    assert response.status_code == 404


# ─── Query Parameter Validation ──────────────────────────────

def test_filter_invalid_status(auth_client):
    response = auth_client.get("/api/v1/tickets/?status=Archived")
    assert response.status_code == 422


def test_filter_invalid_priority(auth_client):
    response = auth_client.get("/api/v1/tickets/?priority=Critical")
    assert response.status_code == 422


def test_get_nonexistent_ticket(auth_client):
    response = auth_client.get("/api/v1/tickets/99999")
    assert response.status_code == 404


# ─── Output Validation ───────────────────────────────────────

def test_response_schema_fields(auth_client):
    """Verify the response includes all expected fields with correct types."""
    create = auth_client.post("/api/v1/tickets/", json=VALID_TICKET)
    data = create.json()
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["description"], str)
    assert isinstance(data["customerName"], str)
    assert isinstance(data["customerEmail"], str)
    assert isinstance(data["status"], str)
    assert isinstance(data["priority"], str)
    assert isinstance(data["createdAt"], str)
    # Status must default to Open
    assert data["status"] == "Open"


def test_error_response_structure(auth_client):
    """Verify that validation errors return structured error objects."""
    response = auth_client.post("/api/v1/tickets/", json={"title": ""})
    assert response.status_code == 422
    body = response.json()
    assert "errors" in body
    assert isinstance(body["errors"], list)
    assert len(body["errors"]) > 0
    # Each error should have field, message, type
    for err in body["errors"]:
        assert "field" in err
        assert "message" in err
        assert "type" in err
