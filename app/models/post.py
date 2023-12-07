from datetime import datetime as dt

from sqlalchemy import ForeignKey, String, orm
from sqlalchemy.orm import Mapped, mapped_column

from app.core import Base, settings
from app.models.user import User


class Post(Base):
    title: Mapped[str] = mapped_column(
        String(settings.title_max_length), unique=True, index=True)
    content: Mapped[str] = mapped_column(String(settings.content_max_length))
    created: Mapped[dt] = mapped_column(default=dt.now)
    updated: Mapped[dt | None]
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    author: Mapped[User] = orm.relationship(lazy='joined')

    def __repr__(self) -> str:
        return (
            f'\ntitle: {self.title},'
            f'\ncontent: {self.content[:100]},'
            f'\ncreated: {self.created},'
            f'\nupdated: {self.updated},'
            f'\nlikes: {self.likes},'
            f'\ndislikes: {self.dislikes},'
            f'\nauthor_id: {self.author_id}.\n'
        )
