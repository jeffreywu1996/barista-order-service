from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Enum, text
from sqlmodel import Field, SQLModel


class OrderStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    INACTIVE = "inactive"
    DELETED = "deleted"

class CoffeeType(str, Enum):
    AMERICANO = "americano"
    ESPRESSO = "espresso"
    LATTE = "latte"
    CAPPUCCINO = "cappuccino"

class UUIDModel(SQLModel):
    class Config:
        arbitrary_types_allowed = True
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default": text("current_timestamp(0)")},
    )
