from datetime import datetime
from typing import List, Tuple, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing_funds(
    investment_object: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    """Invest funds into a charity/donation with amounts control."""
    invested_model, not_invested_objects = await determine_investment_model(
        investment_object, session)
    available_funds = investment_object.full_amount
    for obj in not_invested_objects:
        remaining_funds_needed = obj.full_amount - obj.invested_amount
        investment = min(remaining_funds_needed, available_funds)
        obj.invested_amount += investment
        investment_object.invested_amount += investment
        if obj.full_amount == obj.invested_amount:
            await mark_fully_invested(obj)
        available_funds -= investment
        if not available_funds:
            await mark_fully_invested(investment_object)
            break
    await session.commit()
    return investment_object


async def determine_investment_model(
    investment_object: Union[CharityProject, Donation],
    session: AsyncSession
) -> Tuple[Union[CharityProject, Donation], List[Union[CharityProject, Donation]]]:
    """Determine the Charity/Donation model with amounts control."""
    if isinstance(investment_object, Donation):
        invested_model = CharityProject
    else:
        invested_model = Donation
    query = select(invested_model).where(invested_model.fully_invested == False) # noqa
    not_invested_objects = await session.execute(query)
    not_invested_objects = not_invested_objects.scalars().all()
    return invested_model, not_invested_objects


async def mark_fully_invested(obj: Union[CharityProject, Donation]) -> None:
    """Mark a Charity/Donation as fully invested."""
    obj.fully_invested = True
    obj.close_date = datetime.now()
