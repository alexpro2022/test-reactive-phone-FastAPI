from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi import Request, Response  # noqa
# from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.core import Base, get_async_session, settings  # get_aioredis
from app.main import app
from app.models import Post, User  # noqa
# from app.repositories import DishRepository, MenuRepository, SubmenuRepository  # noqa
from app.repositories.base_db_repository import CRUDBaseRepository  # noqa
from app.schemas import *  # noqa

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


async def override_get_async_session() -> Generator[Any, Any, None]:
    async with TestingSessionLocal() as session:
        yield session


'''
async def override_get_aioredis() -> AsyncGenerator[FakeRedis, Any]:
    r = FakeRedis()
    yield r
    await r.flushall()
'''


app.dependency_overrides[get_async_session] = override_get_async_session
# app.dependency_overrides[get_aioredis] = override_get_aioredis


@pytest_asyncio.fixture(autouse=True)
async def init_db() -> AsyncGenerator[None, Any]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

'''
# --- Fixtures for endpoints testing -----------------------------------------------
@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture
async def menu(async_client: AsyncClient) -> Response:
    menu = await async_client.post(d.ENDPOINT_MENU, json=d.MENU_POST_PAYLOAD)
    assert menu.status_code == 201, (menu.headers, menu.content)
    yield menu


@pytest_asyncio.fixture
async def submenu(async_client: AsyncClient, menu: Response) -> Response:
    assert menu.status_code == 201, (menu.headers, menu.content)
    submenu = await async_client.post(d.ENDPOINT_SUBMENU, json=d.SUBMENU_POST_PAYLOAD)
    assert submenu.status_code == 201, (submenu.headers, submenu.content)
    yield submenu


@pytest_asyncio.fixture
async def dish(async_client: AsyncClient, submenu: Response) -> Response:
    assert submenu.status_code == 201, (submenu.headers, submenu.content)
    dish = await async_client.post(d.ENDPOINT_DISH, json=d.DISH_POST_PAYLOAD)
    assert dish.status_code == 201, (dish.headers, dish.content)
    yield dish
'''


'''
@pytest_asyncio.fixture
async def get_menu_repo(get_test_session: AsyncSession) -> Generator[MenuRepository, Any, None]:
    yield MenuRepository(get_test_session)


@pytest_asyncio.fixture
async def get_submenu_repo(get_test_session: AsyncSession) -> Generator[SubmenuRepository, Any, None]:
    yield SubmenuRepository(get_test_session)


@pytest_asyncio.fixture
async def get_dish_repo(get_test_session: AsyncSession) -> Generator[DishRepository, Any, None]:
    yield DishRepository(get_test_session)





@pytest_asyncio.fixture
async def get_menu_service(get_test_session: AsyncSession, get_test_redis: FakeRedis) -> Generator[MenuService, Any, None]:
    yield MenuService(get_test_session, get_test_redis, None)


@pytest_asyncio.fixture
async def get_submenu_service(get_test_session: AsyncSession, get_test_redis: FakeRedis) -> Generator[SubmenuService, Any, None]:
    yield SubmenuService(get_test_session, get_test_redis, None)


@pytest_asyncio.fixture
async def get_dish_service(get_test_session: AsyncSession, get_test_redis: FakeRedis) -> Generator[DishService, Any, None]:
    yield DishService(get_test_session, get_test_redis, None)
'''
