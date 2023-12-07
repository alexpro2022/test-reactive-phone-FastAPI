from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fakeredis.aioredis import FakeRedis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.repositories import CRUDBaseRepository
from app.services import BaseService
from tests.base_services.data import Base, Data
from tests.conftest import pytest_mark_anyio as pm_anyio

pytest_mark_anyio = pm_anyio

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


# --- Fixtures for repositories testing -----------------------------------------------
@pytest_asyncio.fixture
async def get_test_session() -> Generator[Any, Any, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def get_test_redis() -> AsyncGenerator[FakeRedis, Any]:
    r = FakeRedis()
    yield r
    await r.flushall()


@ pytest.fixture
def get_test_obj() -> Data.model:
    data = {}
    data['id'] = 1
    data.update(Data.post_payload)
    return Data.model(**data)
