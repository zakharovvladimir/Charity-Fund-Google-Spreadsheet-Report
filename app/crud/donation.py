from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """CRUD for Donation model."""
    def __init__(self, model):
        super().__init__(model)

    async def get_user_donations(self,
                                 user: User,
                                 session: AsyncSession) -> List[Donation]:
        """Retrieve users' donations."""
        query = select([self.model]).where(self.model.user_id == user.id)
        result = await session.execute(query)
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
