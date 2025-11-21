from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/problems/{problem_id}/test-cases", response_model=List[schemas.TestCasePublic])
def list_visible_test_cases_for_problem(
    *,
    db: Session = Depends(get_db),
    problem_id: UUID,
):
    # ensure problem exists
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")

    cases = (
        db.query(models.TestCase)
        .filter(models.TestCase.problem_id == problem_id, models.TestCase.is_hidden == False)  # noqa: E712
        .order_by(models.TestCase.weight.desc(), models.TestCase.id)
        .all()
    )
    return cases


# --- Admin/internal test-case management ---


@router.post(
    "/problems/{problem_id}/test-cases",
    response_model=schemas.TestCaseInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_test_case_for_problem(
    *,
    db: Session = Depends(get_db),
    problem_id: UUID,
    test_case_in: schemas.TestCaseCreate,
):
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")

    case = models.TestCase(problem_id=problem_id, **test_case_in.model_dump())
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@router.get("/test-cases/{test_case_id}", response_model=schemas.TestCaseInDB)
def get_test_case(*, db: Session = Depends(get_db), test_case_id: UUID):
    case = db.query(models.TestCase).filter(models.TestCase.id == test_case_id).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test case not found")
    return case


@router.put("/test-cases/{test_case_id}", response_model=schemas.TestCaseInDB)
@router.patch("/test-cases/{test_case_id}", response_model=schemas.TestCaseInDB)
def update_test_case(
    *,
    db: Session = Depends(get_db),
    test_case_id: UUID,
    test_case_in: schemas.TestCaseUpdate,
):
    case = db.query(models.TestCase).filter(models.TestCase.id == test_case_id).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test case not found")

    update_data = test_case_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)

    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@router.delete("/test-cases/{test_case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_case(*, db: Session = Depends(get_db), test_case_id: UUID):
    case = db.query(models.TestCase).filter(models.TestCase.id == test_case_id).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test case not found")

    db.delete(case)
    db.commit()
    return None
