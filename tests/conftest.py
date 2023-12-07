from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fakeredis.aioredis import FakeRedis
# from fastapi import Request, Response  # noqa
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.core import (Base, current_user, get_aioredis, get_async_session,
                      settings)
from app.main import app
from app.models import Post, User  # noqa
from app.repositories.base_db_repository import CRUDBaseRepository  # noqa
from app.schemas import *  # noqa
from tests.integration_tests.utils import create_post

from .fixtures import data as d

# from app.services import BaseService  # noqa
# from app.celery_tasks.utils import FILE_PATH  # noqa


# pytest_plugins = ("celery.contrib.pytest", )

pytest_mark_anyio = pytest.mark.asyncio
# pytest_mark_anyio = pytest.mark.anyio

engine = create_async_engine('sqlite+aiosqlite:///./test.db',
                             connect_args={'check_same_thread': False})

TestingSessionLocal = async_sessionmaker(expire_on_commit=False,
                                         autocommit=False,
                                         autoflush=False,
                                         bind=engine)


@pytest_asyncio.fixture(autouse=True)
async def init_db() -> AsyncGenerator[None, Any]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_async_session() -> Generator[AsyncSession, Any, None]:
    async with TestingSessionLocal() as session:
        yield session


async def override_get_aioredis() -> Generator[FakeRedis, Any, None]:
    r = FakeRedis()
    yield r
    await r.flushall()


app.dependency_overrides[get_async_session] = override_get_async_session
app.dependency_overrides[get_aioredis] = override_get_aioredis


# --- Fixtures for repositories testing in unit_tests -----------
@pytest_asyncio.fixture
async def get_test_session() -> Generator[AsyncSession, Any, None]:
    async for session in override_get_async_session():
        yield session


@pytest_asyncio.fixture
async def get_test_redis() -> Generator[FakeRedis, Any, None]:
    async for aioredis in override_get_aioredis():
        yield aioredis


# --- Fixtures for endpoints testing --------------------------------
@pytest_asyncio.fixture
async def async_client() -> Generator[AsyncClient, Any, None]:
    async with AsyncClient(app=app, base_url='http://testserver') as ac:
        yield ac


@pytest.fixture
def admin_user() -> Generator[None, Any, None]:
    app.dependency_overrides[current_user] = lambda: User(
        id=1,
        is_active=True,
        is_verified=True,
        is_superuser=True,
    )
    yield
    app.dependency_overrides[current_user] = current_user


@pytest_asyncio.fixture
async def new_post(async_client) -> dict[str, str]:
    return await create_post(async_client)
