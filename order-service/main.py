import uuid
from fastapi import FastAPI

app = FastAPI()

db = dict()


@app.get("/v1/order/{order_id}")
async def get_order(order_id: int):
    if order_id not in db:
        return {"message": "Order not found"}
    return {"order_id": order_id, "status": db[order_id]}


@app.post("/v1/order")
async def create_order():
    db.update(
        {"order_id": uuid.uuid4().hex, "status": "created"}
    )
    return {"message": "Hello World"}
