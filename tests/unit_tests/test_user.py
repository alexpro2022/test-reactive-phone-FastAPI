import pytest

from app.core.user import create_admin, create_user
from tests.conftest import User, override_get_async_session, settings


@pytest.mark.asyncio
@pytest.mark.parametrize('is_superuser', (True, False))
async def test_create_user(is_superuser) -> None:
    user: User = await create_user(override_get_async_session,
                                   settings.admin_email,
                                   settings.admin_password,
                                   is_superuser=is_superuser)
    assert user.email == settings.admin_email
    assert user.hashed_password
    assert user.is_superuser == is_superuser


@pytest.mark.asyncio
async def test_create_admin() -> None:
    user: User = await create_admin(override_get_async_session)
    assert user.email == settings.admin_email
    assert user.hashed_password
    assert user.is_superuser
