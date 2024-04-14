import datetime

from sqlalchemy import BIGINT, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from source.database import BaseORM
from source.database.custom_data_types import (
    created_at_base_column,
    string_255,
    string_500,
    string_2000,
    updated_at_base_column,
)


class TagORM(BaseORM):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[String] = mapped_column(
        string_255,
        nullable=False,
    )
    created_at: Mapped[datetime.datetime] = created_at_base_column()
    updated_at: Mapped[datetime.datetime] = updated_at_base_column()


class FeatureORM(BaseORM):
    __tablename__ = "feature"
    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[String] = mapped_column(
        string_255,
        nullable=False,
    )
    created_at: Mapped[datetime.datetime] = created_at_base_column()
    updated_at: Mapped[datetime.datetime] = updated_at_base_column()


class BannerORM(BaseORM):
    __tablename__ = "banner"
    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[String] = mapped_column(
        string_255,
        nullable=False,
    )
    text: Mapped[String] = mapped_column(
        string_2000,
        nullable=False,
    )
    url: Mapped[String] = mapped_column(
        string_500,
        nullable=False,
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    feature_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(
            FeatureORM.id,
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    created_at: Mapped[datetime.datetime] = created_at_base_column()
    updated_at: Mapped[datetime.datetime] = updated_at_base_column()


class BannerTagORM(BaseORM):
    __tablename__ = "banner_tag"
    banner_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(
            BannerORM.id,
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(
            TagORM.id,
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    created_at: Mapped[datetime.datetime] = created_at_base_column()
    updated_at: Mapped[datetime.datetime] = updated_at_base_column()
