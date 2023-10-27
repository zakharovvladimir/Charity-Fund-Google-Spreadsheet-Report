from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """User read properties from the db schema."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """User create properties schema."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """User update properties schema."""
    pass
