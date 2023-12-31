from fastapi import Depends
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(self, password: str, user: User) -> None:
        """Validate user's password."""
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters')


async def get_user_db(
        session: AsyncSession = Depends(
            get_async_session)) -> SQLAlchemyUserDatabase:
    """Get user database."""
    yield SQLAlchemyUserDatabase(session, User)


def get_jwt_strategy() -> JWTStrategy:
    """Get authentication strategy."""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')

auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


async def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    """Get user manager."""
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
