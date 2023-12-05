from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import main_router
from app.core import create_admin, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_admin()
    yield

app = FastAPI(lifespan=lifespan,
              title=settings.app_title,
              description=settings.app_description)

app.include_router(main_router)
