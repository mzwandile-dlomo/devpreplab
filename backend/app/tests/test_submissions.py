import json
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app
from app import models

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/test_devpreplab"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)


def create_problem_and_test_case(db):
    problem = models.Problem(
        title="Add One",
        description="Adds one to x",
        difficulty="easy",
        category="math",
        time_limit=2,
        memory_limit=256,
    )
    db.add(problem)
    db.commit()
    db.refresh(problem)

    case = models.TestCase(
        problem_id=problem.id,
        input={"x": 1},
        expected_output=2,
        is_hidden=False,
        weight=1,
    )
    db.add(case)
    db.commit()

    return problem


def test_create_submission_passes_when_output_matches(monkeypatch, client: TestClient):
    # Arrange: create user + problem + test case directly via DB
    with TestingSessionLocal() as db:
        user = models.User(email="sub@example.com", password_hash="hash")
        db.add(user)
        db.commit()
        db.refresh(user)

        problem = create_problem_and_test_case(db)
        user_id = str(user.id)
        problem_id = str(problem.id)

    # Mock execution to return expected JSON stdout
    from app.utils import execution as exec_mod

    def fake_run_python_code_against_input(*args, **kwargs):  # type: ignore[override]
        return exec_mod.ExecutionOutcome(
            status="passed",
            stdout=json.dumps(2),
            stderr="",
            execution_time_ms=10,
            memory_kb=1024,
        )

    monkeypatch.setattr(
        "app.api.endpoints.submissions.run_python_code_against_input",
        fake_run_python_code_against_input,
    )

    payload = {
        "user_id": user_id,
        "problem_id": problem_id,
        "code": "def solution(x):\n    return x + 1\n",
        "language": "python",
    }

    res = client.post("/api/submissions", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "passed"
    assert data["execution_time"] == 10
    assert data["memory_used"] == 1024


def test_create_submission_fails_when_output_differs(monkeypatch, client: TestClient):
    with TestingSessionLocal() as db:
        user = models.User(email="sub2@example.com", password_hash="hash")
        db.add(user)
        db.commit()
        db.refresh(user)

        problem = create_problem_and_test_case(db)
        user_id = str(user.id)
        problem_id = str(problem.id)

    from app.utils import execution as exec_mod

    def fake_run_python_code_against_input(*args, **kwargs):  # type: ignore[override]
        return exec_mod.ExecutionOutcome(
            status="passed",
            stdout=json.dumps(999),  # wrong answer
            stderr="",
            execution_time_ms=5,
            memory_kb=512,
        )

    monkeypatch.setattr(
        "app.api.endpoints.submissions.run_python_code_against_input",
        fake_run_python_code_against_input,
    )

    payload = {
        "user_id": user_id,
        "problem_id": problem_id,
        "code": "def solution(x):\n    return x + 2\n",
        "language": "python",
    }

    res = client.post("/api/submissions", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "failed"