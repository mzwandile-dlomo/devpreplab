from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/test_devpreplab"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_module(module):  # type: ignore[unused-argument]
    Base.metadata.create_all(bind=engine)


def teardown_module(module):  # type: ignore[unused-argument]
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to the DevPrepLab API"


def test_register_missing_password():
    response = client.post(
        "/api/auth/register",
        json={"email": "nopass@example.com"},
    )
    assert response.status_code == 422


def test_register_invalid_email_format():
    response = client.post(
        "/api/auth/register",
        json={"email": "not-an-email", "password": "password"},
    )
    assert response.status_code == 422


def test_login_with_email_instead_of_username():
    # register a user
    register_response = client.post(
        "/api/auth/register",
        json={"email": "flow@example.com", "password": "flowpassword"},
    )
    assert register_response.status_code == 200

    # attempt login using email (the OAuth2 username field carries the email)
    response = client.post(
        "/api/auth/login",
        data={"username": "flow@example.com", "password": "flowpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
