from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()

GOOGLE_DOCS_URL = 'https://docs.google.com/spreadsheets/d/'


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
    )
async def get_report(
        object: Aiogoogle = Depends(get_service),
        session: AsyncSession = Depends(get_async_session)
) -> str:
    """Generate a report of charities to Google Spreadsheet with URL return."""
    projects = await charity_project.get_by_completion(session)
    spreadsheet_id = await spreadsheets_create(object)
    await set_user_permissions(spreadsheet_id, object)
    await spreadsheets_update_value(spreadsheet_id, projects, object)
    return GOOGLE_DOCS_URL + spreadsheet_id
