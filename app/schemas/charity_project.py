from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityBase(BaseModel):
    """Base charity schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityCreate(CharityBase):
    """Create charity schema."""
    class Config:
        extra = Extra.forbid


class CharityUpdate(CharityBase):
    """Update charity schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = None

    class Config:
        extra = Extra.forbid


class CharityDB(CharityBase):
    """Charity from the db schema."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
