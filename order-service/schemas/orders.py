from datetime import datetime
from uuid import UUID

from db.tables.orders import OrderBase, Order


class OrderCreate(OrderBase):
    ...


class OrderRead(OrderBase):
    id: UUID
    created_at: datetime
    status: str


class OrderPatch(OrderBase):
    ...
