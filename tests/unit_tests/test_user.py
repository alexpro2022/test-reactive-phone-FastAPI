import pytest

from app.core.user import create_admin, create_user
from app.main import lifespan
from tests.conftest import User, override_get_async_session, settings

USER_CREDS = (settings.admin_email, settings.admin_password)

def check_user(user: User, is_superuser: bool = True) -> None:
    assert user.email == settings.admin_email
    assert user.hashed_password
    assert user.is_superuser == is_superuser


@pytest.mark.asyncio
@pytest.mark.parametrize('is_superuser', (True, False))
async def test_create_user(is_superuser) -> None:
    user = await create_user(override_get_async_session, *USER_CREDS, is_superuser)
    check_user(user, is_superuser)


@pytest.mark.asyncio
async def test_create_user_uniqueness() -> None:
    assert await create_user(override_get_async_session, *USER_CREDS)
    assert await create_user(override_get_async_session, *USER_CREDS) is None


@pytest.mark.asyncio
async def test_create_admin() -> None:
    user = await create_admin(override_get_async_session)
    check_user(user)


@pytest.mark.asyncio
async def test_lifespan() -> None:
    async with lifespan('', override_get_async_session) as user:
        check_user(user)
