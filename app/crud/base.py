from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Generate CRUD operations class for models."""
    def __init__(self, model: Type[ModelType]):
        """Initialize CRUD operations class for models."""
        self.model = model

    async def get(self,
                  object_id: int,
                  session: AsyncSession) -> Optional[ModelType]:
        """Get an object by ID."""
        return await session.get(self.model, object_id)

    async def get_all(self, session: AsyncSession) -> List[ModelType]:
        """Get all objects."""
        query = select(self.model)
        db_objs = await session.execute(query)
        return db_objs.scalars().all()

    async def create(self,
                     object_in: CreateSchemaType,
                     session: AsyncSession,
                     user: Optional[User] = None) -> ModelType:
        """Create objects."""
        object_in_data = object_in.dict()
        if user is not None:
            object_in_data['user_id'] = user.id
        db_object = self.model(**object_in_data)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def update(self,
                     db_object: ModelType,
                     object_in: UpdateSchemaType,
                     session: AsyncSession) -> ModelType:
        """Update an existing object."""
        obj_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def delete(self,
                     db_object: ModelType,
                     session: AsyncSession) -> ModelType:
        """Delete an object."""
        await session.delete(db_object)
        await session.commit()
        return db_object

    async def get_not_invested(self,
                               session: AsyncSession) -> List[ModelType]:
        """Get not fully invested objects."""
        query = select(self.model).where(self.model.fully_invested == 0)
        all_not_invested = await session.execute(query)
        return all_not_invested.scalars().all()
