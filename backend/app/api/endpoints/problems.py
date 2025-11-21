from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.ProblemPublic])
def list_problems(
    *,
    db: Session = Depends(get_db),
    difficulty: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
):
    query = db.query(models.Problem)

    if difficulty:
        query = query.filter(models.Problem.difficulty == difficulty)
    if category:
        query = query.filter(models.Problem.category == category)
    if search:
        ilike = f"%{search}%"
        query = query.filter(models.Problem.title.ilike(ilike))

    problems = query.offset(skip).limit(limit).all()
    return problems


@router.get("/random", response_model=schemas.ProblemInDB)
def get_random_problem(
    *,
    db: Session = Depends(get_db),
    difficulty: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
):
    query = db.query(models.Problem)
    if difficulty:
        query = query.filter(models.Problem.difficulty == difficulty)
    if category:
        query = query.filter(models.Problem.category == category)

    problem = query.order_by(func.random()).first()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No problems found")
    return problem


@router.get("/{problem_id}", response_model=schemas.ProblemInDB)
def get_problem(
    *,
    db: Session = Depends(get_db),
    problem_id: UUID,
):
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")
    return problem


@router.post("/", response_model=schemas.ProblemInDB, status_code=status.HTTP_201_CREATED)
def create_problem(
    *,
    db: Session = Depends(get_db),
    problem_in: schemas.ProblemCreate,
):
    # Pydantic v2: use model_dump() instead of dict()/model_dict()
    problem = models.Problem(**problem_in.model_dump())
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


@router.put("/{problem_id}", response_model=schemas.ProblemInDB)
@router.patch("/{problem_id}", response_model=schemas.ProblemInDB)
def update_problem(
    *,
    db: Session = Depends(get_db),
    problem_id: UUID,
    problem_in: schemas.ProblemUpdate,
):
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")

    update_data = problem_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(problem, field, value)

    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


@router.delete("/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_problem(
    *,
    db: Session = Depends(get_db),
    problem_id: UUID,
):
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")

    db.delete(problem)
    db.commit()
    return None
