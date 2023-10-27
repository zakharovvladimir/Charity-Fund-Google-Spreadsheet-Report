from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """Base donation schema."""
    full_amount: PositiveInt
    comment: Optional[str]


class DonationToReveal(DonationBase):
    """Donation to be revealed schema."""
    id: int
    create_date: datetime


class DonationCreate(DonationBase):
    """Donation create schema."""
    pass


class DonationDB(DonationToReveal):
    """Donation from the db schema."""
    class Config:
        orm_mode = True


class DonationCompleteDB(DonationToReveal):
    """Completed donation from the db schema."""
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
