from typing import Annotated, Any, Generator

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)

from app.core.config import settings


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={'ix': 'ix_%(column_0_label)s',
                           'uq': 'uq_%(table_name)s_%(column_0_name)s',
                           'ck': 'ck_%(table_name)s_%(constraint_name)s',
                           'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
                           'pk': 'pk_%(table_name)s'}
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f'\nid: {self.id}\n'


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> Generator[AsyncSession, Any, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session


async_session = Annotated[AsyncSession, Depends(get_async_session)]
