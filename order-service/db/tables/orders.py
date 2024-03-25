from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from uuid import UUID

from db.tables.base_class import StatusEnum, TimestampModel, UUIDModel


class OrderBase(SQLModel):
    amount: int = Field(nullable=False)
    description: str = Field(nullable=False)


class Order(OrderBase, UUIDModel, TimestampModel, table=True):
    status: StatusEnum = Field(default=StatusEnum.inactive)

    __tablename__ = "orders"
