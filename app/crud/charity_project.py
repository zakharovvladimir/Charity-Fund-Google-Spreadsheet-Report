from typing import Optional

from sqlalchemy import select

from app.crud.base import AsyncSession, CRUDBase, ModelType
from app.models.charity_project import CharityProject


class CharityCRUD(CRUDBase):
    """CRUD operations for Charity model."""
    def __init__(self, model: ModelType):
        super().__init__(model)

    async def exists_by_name(self,
                             name: str,
                             session: AsyncSession) -> Optional[ModelType]:
        """Check if a charity name exists."""
        query = select([self.model]).where(self.model.name == name)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_completion(self, session: AsyncSession):
        """Get fully invested charities."""
        query = select([self.model]).where(
            (self.model.fully_invested == 1) &
            (self.model.close_date > self.model.create_date)
        ).order_by(self.model.close_date - self.model.create_date)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_invested_amount(self,
                                  project_id: int,
                                  session: AsyncSession) -> int:
        """Get the invested amount of a charity."""
        query = select([self.model.invested_amount]).where(self.model.id == project_id)
        result = await session.execute(query)
        return result.scalar_one()

    async def get_fully_invested(self,
                                 project_id: int,
                                 session: AsyncSession) -> bool:
        """Check if a charity is fully invested."""
        query = select([self.model.fully_invested]).where(self.model.id == project_id)
        result = await session.execute(query)
        return result.scalar_one()


charity_crud = CharityCRUD(CharityProject)
