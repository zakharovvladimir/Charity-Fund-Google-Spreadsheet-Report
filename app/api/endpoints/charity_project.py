from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import validators
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.schemas.charity_project import (CharityCreate,
                                         CharityDB,
                                         CharityUpdate)
from app.services.investment import investing_funds

NOT_FOUND_CHARITIES = 'Созданные проекты не найдены'
CANNOT_BE_DELETED = 'В проект были внесены средства, не подлежит удалению!'

router = APIRouter()


@router.get('/',
            response_model=List[CharityDB],
            response_model_exclude_none=True)
async def get_all_charities(
    session: AsyncSession = Depends(get_async_session)
):
    """Get all charities."""
    charities = await charity_crud.get_all(session)
    if not charities:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_CHARITIES)
    return charities


@router.post('/',
             response_model=CharityDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)])
async def create_charity(charity: CharityCreate,
                         session: AsyncSession = Depends(get_async_session)):
    """Create new charities."""
    await validators.check_name_duplicate(charity.name, session)
    created_charity = await charity_crud.create(charity, session)
    await investing_funds(created_charity, session)
    await session.refresh(created_charity)
    return created_charity


@router.patch('/{project_id}',
              response_model=CharityDB,
              dependencies=[Depends(current_superuser)])
async def update_charity(project_id: int,
                         object_in: CharityUpdate,
                         session: AsyncSession = Depends(get_async_session)):
    """Update existing charities."""
    charity = await validators.check_charity_exists(project_id, session)
    await validators.charity_closed(project_id, session)
    if object_in.full_amount is not None:
        await validators.check_full_amount_update(project_id,
                                                  object_in.full_amount,
                                                  session)
    if object_in.name is not None:
        await validators.check_name_duplicate(object_in.name, session)
    charity = await charity_crud.update(charity, object_in, session)
    await investing_funds(charity, session)
    await session.refresh(charity)
    return charity


@router.delete('/{project_id}',
               response_model=CharityDB,
               dependencies=[Depends(current_superuser)])
async def delete_charity(project_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    """Delete existing charities."""
    charity = await validators.check_charity_exists(project_id, session)
    if charity.invested_amount > 0:
        raise HTTPException(status_code=400, detail=CANNOT_BE_DELETED)
    return await charity_crud.delete(charity, session)
