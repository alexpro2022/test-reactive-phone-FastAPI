import logging
from contextlib import asynccontextmanager as acm
from typing import Annotated

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pydantic import EmailStr

from app.core import async_session, get_async_session, settings
from app.models import User
from app.schemas.user import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(self, password: str, user: User | UserCreate) -> None:
        if len(password) < settings.password_length:
            raise InvalidPasswordException(
                f'Пароль должен быть длиной не менее '
                f'{settings.password_length} символов.')
        if user.email in password:
            raise InvalidPasswordException(
                'В пароле не должно содержаться e-mail.')

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_db(session: async_session):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_key, lifetime_seconds=settings.token_lifetime)


auth_backend = AuthenticationBackend(name=settings.auth_backend_name,
                                     transport=BearerTransport(
                                         tokenUrl=settings.token_url),
                                     get_strategy=get_jwt_strategy)
fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
authorized = Annotated[User, Depends(current_user)]
admin = Annotated[User, Depends(current_superuser)]

# Create superuseruser programmatically
get_async_session_context = acm(get_async_session)
get_user_db_context = acm(get_user_db)
get_user_manager_context = acm(get_user_manager)


async def create_user(email: EmailStr, password: str, is_superuser: bool = False):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(UserCreate(
                        email=email,
                        password=password,
                        is_superuser=is_superuser))
                    logger.info('Админ создан')
    except UserAlreadyExists:
        logger.info('Админ уже существует')


async def create_admin():
    if all((settings.admin_email, settings.admin_password)):
        await create_user(email=settings.admin_email,
                          password=settings.admin_password,
                          is_superuser=True)
