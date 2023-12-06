from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from tests.base_services.conftest import BaseService, CRUDBaseRepository

MIN_LEN = 3
MAX_LEN = 50


class Base(DeclarativeBase):
    pass


class Model(Base):
    __tablename__ = 'test_model'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]


class SchemaCreate(BaseModel):
    title: str = Field(max_length=MAX_LEN)
    description: str = Field(max_length=MAX_LEN)
    model_config = ConfigDict(str_min_length=MIN_LEN)


class SchemaUpdate(SchemaCreate):
    title: str | None = Field(None, max_length=MAX_LEN)
    description: str | None = Field(None, max_length=MAX_LEN)


class Data:
    model = Model
    create_schema = SchemaCreate
    update_schema = SchemaUpdate
    field_names = ('id', 'title', 'description')
    post_payload = {'title': 'My created object',
                    'description': 'My created object description'}
    update_payload = {'title': 'My updated object',
                      'description': 'My updated object description'}


class CRUD(CRUDBaseRepository):

    def is_update_allowed(self, obj, payload) -> None:
        pass

    def is_delete_allowed(self, obj) -> None:
        pass


class Service(BaseService):

    async def set_cache_on_create(self, obj) -> None:
        await super().set_cache(obj)

    async def set_cache_on_update(self, obj) -> None:
        await super().set_cache(obj)

    async def set_cache_on_delete(self, obj) -> None:
        await self.redis.delete_obj(obj)
