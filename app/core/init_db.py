from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate


async def create_user_manager(email: EmailStr,
                              password: str,
                              is_superuser: bool = False):
    """Create a FastAPI Users user."""
    async with get_async_session() as session:
        async with get_user_db(session) as user_db:
            async with get_user_manager(user_db) as user_manager:
                try:
                    user = UserCreate(email=email,
                                      password=password,
                                      is_superuser=is_superuser)
                    created_user = await user_manager.create(user)
                    return created_user
                except UserAlreadyExists:
                    pass


async def create_first_superuser():
    """Create a superuser."""
    if settings.first_superuser_email and settings.first_superuser_password:
        await create_user_manager(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
