import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from db.tables.orders import Order

logger = logging.getLogger(__name__)

engine = create_engine(
    url=settings.sync_database_url,
    echo=settings.db_echo_log,
)

async_engine = create_async_engine(
    url=settings.async_database_url,
    echo=settings.db_echo_log,
    future=True,
)

async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)



def create_order():
    logger.info('Creating first order. Init db.')
    order = Order(coffee_type="latte", quantity=0, description="First Order", status="deleted")

    with Session(engine) as session:
        session.add(order)
        session.commit()


def init_tables_db():
    """
    Initialize tables if not exists
    """
    with Session(engine) as session:
        try:
            first_order = session.exec(
                select(Order).where(Order.description == "First Order")
            ).first()
        except Exception as e:
            first_order = None

    if not first_order:
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        create_order()
