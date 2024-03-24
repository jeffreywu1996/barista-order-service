import logging
from fastapi import FastAPI, status

from api.router import router
from core.config import settings
from db.sessions import init_tables

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')


app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(router, prefix=settings.api_prefix)

@app.on_event("startup")
async def on_startup():
    init_tables()


@app.get("/")
async def root():
    return {"Say": "Hello!"}


@app.get("/init_tables", status_code=status.HTTP_200_OK, name="init_tables")
async def init_tables():
    init_tables()
