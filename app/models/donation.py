from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text

from app.core.db import Base


class Donation(Base):
    """Donations in the db."""
    __tablename__ = 'donation'

    name: str = Column(Text, nullable=True)
    description: str = Column(Text, nullable=True)
    user_id: int = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment: str = Column(Text, nullable=True)
    full_amount: int = Column(Integer, nullable=False)
    invested_amount: int = Column(Integer, default=0)
    fully_invested: bool = Column(Boolean, default=False)
    create_date: datetime = Column(DateTime, default=datetime.now)
    close_date: datetime = Column(DateTime, nullable=True)
