import logging
from contextlib import asynccontextmanager
from typing import Annotated, Generator

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pydantic import EmailStr

from app.core import async_session, get_async_session, settings
from app.models import User
from app.schemas.user import UserCreate
from app.validators import (password_content_validator,
                            password_length_validator)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(self, password: str, user: User | UserCreate) -> None:
        password_length_validator(password)
        password_content_validator(password, user.email)

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
async def create_user(
    async_session_generator: Generator, email: EmailStr, password: str, is_superuser: bool = False
) -> User:
    try:
        async with (asynccontextmanager(async_session_generator)() as session,
                    asynccontextmanager(get_user_db)(session) as user_db,
                    asynccontextmanager(get_user_manager)(user_db) as user_manager):
            user = await user_manager.create(UserCreate(email=email, password=password, is_superuser=is_superuser))
    except UserAlreadyExists:
        logger.info('Админ уже существует')
    else:
        logger.info('Админ создан')
        return user


async def create_admin(async_generator: Generator = get_async_session) -> User:
    if all((settings.admin_email, settings.admin_password)):
        return await create_user(async_generator,
                                 email=settings.admin_email,
                                 password=settings.admin_password,
                                 is_superuser=True)
