from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from db.tables.base_class import StatusEnum
from db.tables.orders import Order
from schemas.orders import OrderCreate, OrderPatch, OrderRead


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, order_id: UUID):
        statement = (
            select(Order)
            .where(Order.id == order_id)
            .where(Order.status != StatusEnum.deleted)
        )
        results = await self.session.exec(statement)

        return results.first()

    async def create(self, order_create: OrderCreate) -> OrderRead:
        db_order = Order.from_orm(order_create)
        self.session.add(db_order)
        await self.session.commit()
        await self.session.refresh(db_order)

        return OrderRead(**db_order.dict())

    async def list(self, limit: int = 10, offset: int = 0) -> list[OrderRead]:
        statement = (
            (select(Order).where(Order.status != StatusEnum.deleted))
            .offset(offset)
            .limit(limit)
        )
        results = await self.session.exec(statement)

        return [OrderRead(**order.dict()) for order in results]

    async def get(self, order_id: UUID) -> Optional[OrderRead]:
        db_order = await self._get_instance(order_id)

        if db_order is None:
            raise EntityDoesNotExist

        return OrderRead(**db_order.dict())
