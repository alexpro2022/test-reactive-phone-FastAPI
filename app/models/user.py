from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
