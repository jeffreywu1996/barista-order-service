from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from db.tables.base_class import OrderStatus
from db.tables.orders import Order
from schemas.orders import OrderCreate, OrderPatch, OrderRead


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, order_id: UUID):
        statement = (
            select(Order)
            .where(Order.id == order_id)
            .where(Order.status != OrderStatus.DELETED)
        )
        results = await self.session.exec(statement)

        return results.first()

    async def create(self, order_create: OrderCreate) -> OrderRead:
        db_order = Order.model_validate(order_create)
        self.session.add(db_order)
        await self.session.commit()
        await self.session.refresh(db_order)

        return OrderRead(**db_order.model_dump())

    async def list(self, limit: int = 10, offset: int = 0) -> list[OrderRead]:
        statement = (
            (select(Order).where(Order.status != OrderStatus.DELETED))
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
        self, order_id: UUID, order_patch: OrderPatch
    ) -> Optional[OrderRead]:
        db_order = await self._get_instance(order_id)

        if db_order is None:
            raise EntityDoesNotExist

        order_data = order_patch.model_dump(exclude_unset=True, exclude={"id"})
        for key, value in order_data.items():
            setattr(db_order, key, value)

        self.session.add(db_order)
        await self.session.commit()
        await self.session.refresh(db_order)

        return OrderRead(**db_order.model_dump())

    async def delete(self, transaction_id: UUID) -> None:
        db_order = await self._get_instance(transaction_id)

        if db_order is None:
            raise EntityDoesNotExist

        setattr(db_order, "status", OrderStatus.DELETED)
        self.session.add(db_order)

        await self.session.commit()
