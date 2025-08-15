from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from models.base import Base
from models.db_helper import db_helper
from src.api import router as api_router
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadatacreate_all)
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(api_router, prefix=settings.api_prefix.prefix)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
