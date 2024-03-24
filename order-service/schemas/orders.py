from uuid import UUID

from db.tables.orders import OrderBase


class OrderCreate(OrderBase):
    ...


class OrderRead(OrderBase):
    id: UUID


class OrderPatch(OrderBase):
    ...
