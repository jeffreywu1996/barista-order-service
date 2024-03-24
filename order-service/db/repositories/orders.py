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

    async def create(self, transaction_create: OrderCreate) -> OrderRead:
        db_order = Order.from_orm(transaction_create)
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

    async def patch(
        self, order_id: UUID, transaction_patch: OrderPatch
    ) -> Optional[OrderRead]:
        db_order = await self._get_instance(order_id)

        if db_order is None:
            raise EntityDoesNotExist

        transaction_data = transaction_patch.dict(exclude_unset=True, exclude={"id"})
        for key, value in transaction_data.items():
            setattr(db_order, key, value)

        self.session.add(db_order)
        await self.session.commit()
        await self.session.refresh(db_order)

        return OrderRead(**db_order.dict())

    async def delete(self, order_id: UUID) -> None:
        db_order = await self._get_instance(order_id)

        if db_order is None:
            raise EntityDoesNotExist

        setattr(db_order, "status", StatusEnum.deleted)
        self.session.add(db_order)

        await self.session.commit()
