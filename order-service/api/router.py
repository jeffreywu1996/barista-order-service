from fastapi import APIRouter

from api.routes.orders import router as orders_router

router = APIRouter()

router.include_router(orders_router, prefix="/v1")
