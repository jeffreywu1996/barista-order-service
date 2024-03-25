from datetime import datetime
from uuid import UUID
from pydantic import validator
from sqlmodel import Field, SQLModel

from db.tables.orders import OrderBase, CoffeeType


class OrderCreate(OrderBase):
    ...


class OrderRead(OrderBase):
    id: UUID
    created_at: datetime
    status: str


class OrderPatch(SQLModel):
    status: str
    ...
