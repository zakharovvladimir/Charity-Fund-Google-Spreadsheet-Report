from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings
from app.models import CharityProject

DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'
CURRENT_DATETIME = datetime.now().strftime(DATETIME_FORMAT)
TABLE_HEADERS = ['Название проекта', 'Описание', 'Дата создания', 'Дата закрытия']
ROWS = 50
DOC_TITLE = 'Отчет'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Create a Google Spreadsheet for charities."""
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'{DOC_TITLE} - {CURRENT_DATETIME}', 'locale': 'ru_RU'},
        'sheets': [
            {'properties': {'sheetType': 'GRID',
                            'sheetId': 0,
                            'title': DOC_TITLE,
                            'gridProperties': {'rowCount': ROWS,
                                               'columnCount': len(TABLE_HEADERS)}}}
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheet_id']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Set users' permissions for a Google Spreadsheet."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charities: list[CharityProject],
        wrapper_services: Aiogoogle
) -> str:
    """Update the values for Google Spreadsheet data."""
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = []
    for item in charities:
        row = [
            item.name,
            item.description,
            str(item.close_date, item.create_date)
        ]
        table_values.append(row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': [TABLE_HEADERS] + table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
