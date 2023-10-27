from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCompleteDB, DonationCreate, DonationDB
from app.services.investment import investing_funds

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationCompleteDB],
    response_model_exclude_none=True
)
async def get_all(
    user: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session)
) -> List[DonationCompleteDB]:
    """Retrieve all donations."""
    donations = await donation_crud.get_all(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True
)
async def my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> List[DonationDB]:
    """Retrieve user's donations."""
    donations = await donation_crud.get_user_donations(user=user, session=session)
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> DonationDB:
    """Create new donations."""
    create_donation = await donation_crud.create(donation, session, user)
    await investing_funds(create_donation, session)
    await session.refresh(create_donation)
    return create_donation
