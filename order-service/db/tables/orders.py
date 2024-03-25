from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import validator

from db.tables.base_class import OrderStatus, TimestampModel, UUIDModel, CoffeeType

import logging
logger = logging.getLogger(__name__)

class OrderBase(SQLModel):
    class Config:
        arbitrary_types_allowed = True
    # coffee_type: CoffeeType = Field(nullable=False)
    coffee_type: str = Field(nullable=False, description="The type of coffee for the order")
    quantity: int = Field(nullable=False)
    description: str = Field(default="No description", nullable=False)

    # @validator('coffee_type', pre=True)
    # def parse_coffee_type(cls, v):
    #     if isinstance(v, str):
    #         try:
    #             if v not in ['latte', 'cappuccino', 'espresso', 'americano']:  # FIXME: fix with proper enum validation
    #                 raise ValueError(f"Invalid coffee type: {v}")
    #             return CoffeeType(v)
    #         except ValueError:
    #             raise ValueError(f"Invalid coffee type: {v}")
    #     return v


class Order(OrderBase, UUIDModel, TimestampModel, table=True):
    status: OrderStatus = Field(default=OrderStatus.CREATED)

    __tablename__ = "orders"
