from typing import Any, Generic, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс для CRUD операций произвольных моделей."""
    OBJECT_ALREADY_EXISTS = 'Object with such a unique values already exists.'
    NOT_FOUND = 'Object(s) not found.'

    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
        self.order_by = self.model.id

    def set_order_by(self, attr) -> None:
        pass

# === Hooks ===
    def has_permission(self, obj: ModelType, user) -> None:
        """Check for user permission and raise exception if not allowed."""
        raise NotImplementedError('has_permission() must be implemented.')

    def is_update_allowed(self, obj: ModelType, payload: dict) -> None:
        """Check for custom conditions and raise exception if not allowed."""
        raise NotImplementedError('is_update_allowed() must be implemented.')

    def is_delete_allowed(self, obj: ModelType) -> None:
        """Check for custom conditions and raise exception if not allowed."""
        raise NotImplementedError('is_delete_allowed() must be implemented.')

# === Read ===
    async def __get_by_attributes(self, *, all: bool = False, **kwargs) -> list[ModelType] | ModelType | None:
        query = select(self.model).filter_by(
            **kwargs) if kwargs else select(self.model)
        result = await self.session.scalars(query.order_by(self.order_by))
        return result.all() if all else result.first()

    async def _get_all_by_attrs(self, exception: bool = False, **kwargs) -> list[ModelType] | None:
        """Raises `NOT_FOUND` exception if no objects are found and `exception=True`
           else returns `None` else returns list of found objects."""
        objects = await self.__get_by_attributes(all=True, **kwargs)
        if not objects:
            if exception:
                raise HTTPException(status.HTTP_404_NOT_FOUND, self.NOT_FOUND)
            return None
        return objects

    async def _get_by_attrs(self, exception: bool = False, **kwargs) -> ModelType | None:
        """Raises `NOT_FOUND` exception if no object is found and `exception=True`."""
        object = await self.__get_by_attributes(**kwargs)
        if object is None and exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND, self.NOT_FOUND)
        return object  # type: ignore

    async def get(self, pk: int) -> ModelType | None:
        return await self._get_by_attrs(id=pk)

    async def get_or_404(self, pk: int) -> ModelType:
        return await self._get_by_attrs(id=pk, exception=True)  # type: ignore

    async def get_all(self, exception: bool = False) -> list[ModelType] | None:
        return await self._get_all_by_attrs(exception=exception)

# === Create, Update, Delete ===
    async def _save(self, obj: ModelType) -> ModelType:
        """Raises `BAD_REQUEST` exception if object already exists in DB. """
        self.session.add(obj)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                self.OBJECT_ALREADY_EXISTS)
        await self.session.refresh(obj)
        return obj

    async def create(self, payload: CreateSchemaType, **kwargs) -> ModelType:
        create_data = payload.model_dump()
        if kwargs:
            create_data.update(kwargs)
        return await self._save(self.model(**create_data))

    async def update(self, pk: int, payload: UpdateSchemaType, user: Any | None = None, **kwargs) -> ModelType:
        obj = await self.get_or_404(pk)
        if user is not None:
            self.has_permission(obj, user)
        update_data = payload.model_dump(exclude_unset=True,
                                         exclude_none=True,
                                         exclude_defaults=True)
        if kwargs:
            update_data.update(kwargs)
        self.is_update_allowed(obj, update_data)
        for key, value in update_data.items():
            setattr(obj, key, value)
        return await self._save(obj)

    async def delete(self, pk: int, user: Any | None = None) -> ModelType:
        obj = await self.get_or_404(pk)
        if user is not None:
            self.has_permission(obj, user)
        self.is_delete_allowed(obj)
        await self.session.delete(obj)
        await self.session.commit()
        return obj
