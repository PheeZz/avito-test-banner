from sqlalchemy.orm import DeclarativeBase


class BaseORM(DeclarativeBase):
    """
    Common base class for all ORM objects
    """

    __table_args__ = {"schema": "public"}
