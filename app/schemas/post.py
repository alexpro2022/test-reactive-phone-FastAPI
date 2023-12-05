from datetime import datetime as dt

from pydantic import BaseModel, ConfigDict, Field

from app.core import settings
from app.schemas.user import UserRead


class PostIn(BaseModel):
    title: str = Field(max_length=settings.title_max_length,
                       json_schema_extra={'example': 'New post title.'})
    content: str = Field(max_length=settings.content_max_length, json_schema_extra={
                         'example': 'New post content.'})
    model_config = ConfigDict(str_min_length=settings.post_min_anystr_length)


class PostCreate(PostIn):
    pass


class PostUpdate(PostIn):
    title: str | None = Field(
        None, max_length=settings.title_max_length, json_schema_extra={'example': 'Updated post title.'})
    content: str | None = Field(
        None, max_length=settings.content_max_length, json_schema_extra={'example': 'Updated post content.'})


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created: dt
    updated: dt | None = None
    likes: int
    dislikes: int
    author: UserRead
    model_config = ConfigDict(from_attributes=True)
