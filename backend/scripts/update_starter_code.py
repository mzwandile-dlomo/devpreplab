"""Update existing problems with starter code."""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.problem import Problem

def update_starter_code():
    db: Session = SessionLocal()
    try:
        starter_codes = {
            "Two Sum": """def solution(nums, target):
    \"\"\"
    Given an array of integers nums and an integer target,
    return indices of the two numbers such that they add up to target.

    Args:
        nums: List of integers
        target: Target sum

    Returns:
        dict with key 'indices' containing list of two indices [i, j]
    \"\"\"
    # TODO: implement your solution here
    return {"indices": [0, 1]}
""",
            "Add Two Numbers": """def solution(l1, l2):
    \"\"\"
    Add two numbers represented as linked lists (arrays in reverse order).

    Args:
        l1: List of digits in reverse order
        l2: List of digits in reverse order

    Returns:
        dict with key 'sum' containing list of digits in reverse order
    \"\"\"
    # TODO: implement your solution here
    return {"sum": [0]}
""",
            "Median of Two Sorted Arrays": """def solution(nums1, nums2):
    \"\"\"
    Find the median of two sorted arrays.

    Args:
        nums1: First sorted array
        nums2: Second sorted array

    Returns:
        dict with key 'median' containing the median value (float)
    \"\"\"
    # TODO: implement your solution here
    return {"median": 0.0}
""",
        }

        for title, starter_code in starter_codes.items():
            problem = db.query(Problem).filter(Problem.title == title).first()
            if problem:
                problem.starter_code = starter_code
                print(f"Updated starter code for: {title}")
            else:
                print(f"Problem not found: {title}")

        db.commit()
        print("Successfully updated all problems with starter code.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_starter_code()
