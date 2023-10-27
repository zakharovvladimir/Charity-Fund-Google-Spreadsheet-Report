from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

RESTRICTED_DELETE = 'Удаление пользователей запрещено!'

router = APIRouter()

auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)

router.include_router(auth_router, prefix='/auth/jwt')
router.include_router(register_router, prefix='/auth')
router.include_router(users_router, prefix='/users')


@router.delete('/users/{id}', deprecated=True)
def delete_user(id: str):
    """Deleting users' profiles."""
    raise HTTPException(
        status_code=405,
        detail=RESTRICTED_DELETE
    )
