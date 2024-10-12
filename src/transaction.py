import datetime as dt
import uuid
from typing import Literal, Optional

from pydantic import BaseModel, Field, PositiveFloat, field_validator


class Transaction(BaseModel, extra="ignore"):
    id: str = Field(default_factory=uuid.uuid4)
    amount: PositiveFloat
    date: dt.date = Field(default_factory=dt.date.today),
    type: Literal["income", "expense"]
    category: str
    description: Optional[str] = Field(default=None, validate_default=False)

    @field_validator("description")
    @classmethod
    def validate_description(cls, description: Optional[str]) -> Optional[str]:
        if description is None:
            return description
        if len(description) == 0:
            raise ValueError("Description cannot be empty")
        if len(description) > 100:
            raise ValueError("Description must be less than 100 characters")
        return description
