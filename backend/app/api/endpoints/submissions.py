from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.database import get_db
from app.core.security import get_current_user
from app.utils.execution import run_python_code_against_input, ExecutionOutcome
import json

router = APIRouter()


@router.post("/preview", response_model=schemas.SubmissionResult)
def preview_submission(
    *,
    db: Session = Depends(get_db),
    submission_in: schemas.SubmissionPreview,
):
    """Run code against visible test cases without persisting a submission.

    This is used for anonymous practice attempts that should not be stored.
    """
    # Ensure problem exists
    problem = (
        db.query(models.Problem)
        .filter(models.Problem.id == submission_in.problem_id)
        .first()
    )
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )

    if submission_in.language != "python":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Python submissions are supported in this phase.",
        )

    cases = (
        db.query(models.TestCase)
        .filter(
            models.TestCase.problem_id == problem.id,
            models.TestCase.is_hidden == False,  # noqa: E712
        )
        .all()
    )
    if not cases:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No visible test cases configured for this problem.",
        )

    overall_status = "passed"
    last_outcome: ExecutionOutcome | None = None

    for case in cases:
        outcome = run_python_code_against_input(
            code=submission_in.code,
            test_input=case.input,
            time_limit_seconds=problem.time_limit,
            memory_limit_mb=problem.memory_limit,
        )
        last_outcome = outcome

        if outcome.status not in {"passed", "failed"}:
            overall_status = outcome.status
            break

        try:
            actual = json.loads(outcome.stdout) if outcome.stdout else None
        except json.JSONDecodeError:
            overall_status = "error"
            break

        if actual != case.expected_output:
            overall_status = "failed"
            break

    return schemas.SubmissionResult(
        status=overall_status,
        stdout=last_outcome.stdout if last_outcome else "",
        stderr=last_outcome.stderr if last_outcome else "",
        execution_time_ms=last_outcome.execution_time_ms if last_outcome else None,
        memory_kb=last_outcome.memory_kb if last_outcome else None,
    )


@router.post("/", response_model=schemas.SubmissionInDB, status_code=status.HTTP_201_CREATED)
def create_submission(
    *,
    db: Session = Depends(get_db),
    submission_in: schemas.SubmissionCreate,
):
    # Ensure problem exists
    problem = (
        db.query(models.Problem)
        .filter(models.Problem.id == submission_in.problem_id)
        .first()
    )
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )

    if submission_in.language != "python":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Python submissions are supported in this phase.",
        )

    # For Phase 3 we will run only against visible test cases
    cases = (
        db.query(models.TestCase)
        .filter(
            models.TestCase.problem_id == problem.id,
            models.TestCase.is_hidden == False,  # noqa: E712
        )
        .all()
    )

    if not cases:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No visible test cases configured for this problem.",
        )

    overall_status = "passed"
    last_outcome: ExecutionOutcome | None = None

    for case in cases:
        outcome = run_python_code_against_input(
            code=submission_in.code,
            test_input=case.input,
            time_limit_seconds=problem.time_limit,
            memory_limit_mb=problem.memory_limit,
        )
        last_outcome = outcome

        if outcome.status not in {"passed", "failed"}:
            # infrastructure / execution error: bubble up status directly
            overall_status = outcome.status
            break

        # At this level we compare the stdout JSON with expected_output
        try:
            actual = json.loads(outcome.stdout) if outcome.stdout else None
        except json.JSONDecodeError:
            overall_status = "error"
            break

        if actual != case.expected_output:
            overall_status = "failed"
            break

    submission = models.Submission(
        user_id=submission_in.user_id,
        problem_id=submission_in.problem_id,
        code=submission_in.code,
        language=submission_in.language,
        status=overall_status,
        execution_time=last_outcome.execution_time_ms if last_outcome else None,
        memory_used=last_outcome.memory_kb if last_outcome else None,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission


@router.get("/me", response_model=List[schemas.SubmissionInDB])
def list_my_submissions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Return submissions for the currently authenticated user.

    This endpoint demonstrates authorization: the caller only sees their own submissions
    based on the Bearer token.
    """
    submissions = (
        db.query(models.Submission)
        .filter(models.Submission.user_id == current_user.id)
        .order_by(models.Submission.submitted_at.desc())
        .all()
    )
    return submissions


@router.get("/{submission_id}", response_model=schemas.SubmissionInDB)
def get_submission(submission_id: str, db: Session = Depends(get_db)):
    submission = (
        db.query(models.Submission)
        .filter(models.Submission.id == submission_id)
        .first()
    )
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return submission
    """Return submissions for the currently authenticated user.

    This endpoint demonstrates authorization: the caller only sees their own submissions
    based on the Bearer token.
    """
    submissions = (
        db.query(models.Submission)
        .filter(models.Submission.user_id == current_user.id)
        .order_by(models.Submission.submitted_at.desc())
        .all()
    )
    return submissions
