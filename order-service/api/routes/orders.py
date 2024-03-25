from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status, Request

from api.dependencies.repositories import get_repository
from db.errors import EntityDoesNotExist
from db.repositories.orders import OrderRepository
from schemas.orders import OrderCreate, OrderPatch, OrderRead

router = APIRouter()


@router.post(
    "/order",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    name="create_order",
)
async def create_order(
    request: Request,
    order_create: OrderCreate = Body(...),
    repository: OrderRepository = Depends(get_repository(OrderRepository)),
) -> OrderRead:
    order = await repository.create(order_create=order_create)
    request.app.mq.publish(order.model_dump_json(indent=2))
    return order

@router.get(
    "/order",
    response_model=list[Optional[OrderRead]],
    status_code=status.HTTP_200_OK,
    name="get_orders",
)
async def get_orders(
    limit: int = Query(default=10, lte=100),
    offset: int = Query(default=0),
    repository: OrderRepository = Depends(get_repository(OrderRepository)),
) -> list[Optional[OrderRead]]:
    return await repository.list(limit=limit, offset=offset)


@router.get(
    "/order/{order_id}",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
    name="get_order",
)
async def get_order(
    order_id: UUID,
    repository: OrderRepository = Depends(get_repository(OrderRepository)),
) -> OrderRead:
    try:
        await repository.get(order_id=order_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!"
        )

    return await repository.get(order_id=order_id)

@router.delete(
    "/order/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_order",
)
async def delete_order(
    order_id: UUID,
    repository: OrderRepository = Depends(get_repository(OrderRepository)),
) -> None:
    try:
        await repository.get(order_id=order_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="order not found!"
        )

    return await repository.delete(order_id=order_id)


@router.put(
    "/orders/{order_id}",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
    name="delete_order",
)
async def delete_order(
    order_id: UUID,
    order_patch: OrderPatch = Body(...),
    repository: OrderRepository = Depends(get_repository(OrderRepository)),
) -> OrderRead:
    try:
        await repository.get(order_id=order_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="order not found!"
        )

    return await repository.patch(
        order_id=order_id, order_patch=order_patch
    )
