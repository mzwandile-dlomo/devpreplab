import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.models.test_case import TestCase

def seed_problems():
    db: Session = SessionLocal()
    try:
        problems_to_seed = [
            Problem(
                title="Two Sum",
                description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                difficulty="easy",
                category="Arrays",
                time_limit=1,
                memory_limit=256,
                starter_code="""def solution(nums, target):
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
            ),
            Problem(
                title="Add Two Numbers",
                description="You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.",
                difficulty="medium",
                category="Linked Lists",
                time_limit=2,
                memory_limit=512,
                starter_code="""def solution(l1, l2):
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
            ),
            Problem(
                title="Median of Two Sorted Arrays",
                description="Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.",
                difficulty="hard",
                category="Arrays",
                time_limit=3,
                memory_limit=512,
                starter_code="""def solution(nums1, nums2):
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
            ),
        ]

        test_cases_to_seed = {
            "Two Sum": [
                TestCase(input={"nums": [2, 7, 11, 15], "target": 9}, expected_output={"indices": [0, 1]}),
                TestCase(input={"nums": [3, 2, 4], "target": 6}, expected_output={"indices": [1, 2]}),
                TestCase(input={"nums": [3, 3], "target": 6}, expected_output={"indices": [0, 1]}),
            ],
            "Add Two Numbers": [
                TestCase(input={"l1": [2, 4, 3], "l2": [5, 6, 4]}, expected_output={"sum": [7, 0, 8]}),
                TestCase(input={"l1": [0], "l2": [0]}, expected_output={"sum": [0]}),
                TestCase(input={"l1": [9,9,9,9,9,9,9], "l2": [9,9,9,9]}, expected_output={"sum": [8,9,9,9,0,0,0,1]}),
            ],
            "Median of Two Sorted Arrays": [
                TestCase(input={"nums1": [1, 3], "nums2": [2]}, expected_output={"median": 2.0}),
                TestCase(input={"nums1": [1, 2], "nums2": [3, 4]}, expected_output={"median": 2.5}),
            ]
        }

        for problem in problems_to_seed:
            db.add(problem)
            db.flush()  # Flush to get the problem.id
            
            if problem.title in test_cases_to_seed:
                for test_case_data in test_cases_to_seed[problem.title]:
                    test_case_data.problem_id = problem.id
                    db.add(test_case_data)
        
        db.commit()
        print("Successfully seeded problems and their test cases.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_problems()