"""
Plan router
"""

from fastapi import APIRouter, status
from sqlmodel import select

from app.models import Plan
from app.db import SessionDep


# Create router
router = APIRouter()

@router.post(
    '/plans',
    response_model=Plan,
    status_code=status.HTTP_201_CREATED,
    tags=['Plans']
)
async def create_plan(plan_data: Plan, session: SessionDep):
    """
    Create a new plan
    """
    plan = Plan.model_validate(plan_data.model_dump())
    session.add(plan)
    session.commit()
    session.refresh(plan)

    return plan


@router.get(
    '/plans',
    response_model=list[Plan],
    tags=['Plans']
)
async def list_plans(session: SessionDep):
    """
    Get all plans
    """
    query = select(Plan)
    plans_list = session.exec(query).all()

    return plans_list
