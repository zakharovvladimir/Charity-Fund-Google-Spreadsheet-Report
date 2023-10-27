from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_crud

CHARITY_EXISTS = 'Проект с таким именем уже существует!'
CHARITY_NOT_FOUND = 'Проект не найден'
CLOSED_CHARITY = 'Закрытый проект нельзя редактировать!'
AMOUNT_VALIDATION = 'Значение требуемой суммы не может быть меньше внесённой'


async def check_name_duplicate(name: str, session: AsyncSession):
    """Check if a charity's name exists."""
    if await charity_crud.exists_by_name(name, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CHARITY_EXISTS
        )


async def check_charity_exists(id: int, session: AsyncSession):
    """Check if a charity's ID exists."""
    project = await charity_crud.get(id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CHARITY_NOT_FOUND
        )
    return project


async def check_full_amount_update(project_id: int,
                                   updating_full_amount: int,
                                   session: AsyncSession):
    """Check a charity's full amount funding validity."""
    invested_amount = await charity_crud.get_invested_amount(project_id, session)
    if updating_full_amount < invested_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=AMOUNT_VALIDATION
        )


async def charity_closed(project_id: int, session: AsyncSession):
    """Check if a charity is funded and closed."""
    project_closed = await charity_crud.get_fully_invested(project_id, session)
    if project_closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CLOSED_CHARITY
        )
