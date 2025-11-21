import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/test_devpreplab"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def client():
    # Create the tables in the test database
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

    # Drop the tables after tests are done
    Base.metadata.drop_all(bind=engine)


def create_sample_problem(client: TestClient, title: str = "Two Sum", difficulty: str = "easy"):
    response = client.post(
        "/api/problems",
        json={
            "title": title,
            "description": "Sample description",
            "difficulty": difficulty,
            "category": "arrays",
            "time_limit": 2,
            "memory_limit": 256,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_and_get_problem(client: TestClient):
    created = create_sample_problem(client)

    problem_id = created["id"]
    response = client.get(f"/api/problems/{problem_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == problem_id
    assert data["title"] == "Two Sum"
    assert data["difficulty"] == "easy"


def test_list_problems_with_filters(client: TestClient):
    # create multiple problems
    create_sample_problem(client, title="Easy Arrays", difficulty="easy")
    create_sample_problem(client, title="Medium Arrays", difficulty="medium")

    # filter by difficulty
    res_easy = client.get("/api/problems", params={"difficulty": "easy"})
    assert res_easy.status_code == 200
    data_easy = res_easy.json()
    assert all(p["difficulty"] == "easy" for p in data_easy)

    # search by title substring
    res_search = client.get("/api/problems", params={"search": "Medium"})
    assert res_search.status_code == 200
    data_search = res_search.json()
    assert any("Medium" in p["title"] for p in data_search)


def test_update_and_delete_problem(client: TestClient):
    created = create_sample_problem(client, title="Old Title")
    problem_id = created["id"]

    # update title via PATCH
    res_update = client.patch(
        f"/api/problems/{problem_id}", json={"title": "New Title", "difficulty": "medium"}
    )
    assert res_update.status_code == 200
    updated = res_update.json()
    assert updated["title"] == "New Title"
    assert updated["difficulty"] == "medium"

    # delete
    res_delete = client.delete(f"/api/problems/{problem_id}")
    assert res_delete.status_code == 204

    # ensure it is gone
    res_get = client.get(f"/api/problems/{problem_id}")
    assert res_get.status_code == 404


def test_random_problem_endpoint(client: TestClient):
    # ensure at least one easy problem exists
    create_sample_problem(client, title="Random Easy", difficulty="easy")

    res = client.get("/api/problems/random", params={"difficulty": "easy"})
    assert res.status_code == 200
    data = res.json()
    assert data["difficulty"] == "easy"


def test_create_and_list_visible_test_cases(client: TestClient):
    problem = create_sample_problem(client, title="With Test Cases")
    problem_id = problem["id"]

    # create a visible and a hidden test case
    res_visible = client.post(
        f"/api/problems/{problem_id}/test-cases",
        json={
            "input": {"nums": [2, 7, 11, 15], "target": 9},
            "expected_output": [0, 1],
            "is_hidden": False,
            "weight": 1,
        },
    )
    assert res_visible.status_code == 201

    res_hidden = client.post(
        f"/api/problems/{problem_id}/test-cases",
        json={
            "input": {"nums": [3, 3], "target": 6},
            "expected_output": [0, 1],
            "is_hidden": True,
            "weight": 1,
        },
    )
    assert res_hidden.status_code == 201

    # visible endpoint should only return non-hidden
    res_list = client.get(f"/api/problems/{problem_id}/test-cases")
    assert res_list.status_code == 200
    cases = res_list.json()
    assert len(cases) == 1
    assert cases[0]["input"]["target"] == 9


def test_get_update_delete_test_case_by_id(client: TestClient):
    problem = create_sample_problem(client, title="Test Case CRUD")
    problem_id = problem["id"]

    res_create = client.post(
        f"/api/problems/{problem_id}/test-cases",
        json={
            "input": {"x": 1},
            "expected_output": 2,
            "is_hidden": False,
            "weight": 1,
        },
    )
    assert res_create.status_code == 201
    case = res_create.json()
    case_id = case["id"]

    # get
    res_get = client.get(f"/api/test-cases/{case_id}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == case_id

    # update
    res_update = client.patch(
        f"/api/test-cases/{case_id}", json={"is_hidden": True, "weight": 5}
    )
    assert res_update.status_code == 200
    updated = res_update.json()
    assert updated["is_hidden"] is True
    assert updated["weight"] == 5

    # delete
    res_delete = client.delete(f"/api/test-cases/{case_id}")
    assert res_delete.status_code == 204

    # ensure gone
    res_get_2 = client.get(f"/api/test-cases/{case_id}")
    assert res_get_2.status_code == 404


def test_problem_not_found_for_test_cases(client: TestClient):
    random_uuid = uuid.uuid4()
    res = client.get(f"/api/problems/{random_uuid}/test-cases")
    assert res.status_code == 404
    assert res.json()["detail"] == "Problem not found"
