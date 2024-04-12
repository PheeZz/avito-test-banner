import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import MappedColumn, mapped_column
import pytz


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(tz=pytz.utc)


def created_at_base_column() -> MappedColumn:
    return mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


def updated_at_base_column() -> MappedColumn:
    return mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )


string_255 = String(255)
string_500 = String(500)
string_2000 = String(2000)
