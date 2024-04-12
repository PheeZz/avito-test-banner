from logging import getLogger
from typing import Iterable

from sqlalchemy import func, select

from source.database import async_session_factory

from . import models, schemas

logger = getLogger(__name__)


class BannerDAO:
    @classmethod
    async def create_banner(cls, banner: schemas.CreateBannerSchema) -> int:
        async with async_session_factory() as session:
            async with session.begin():
                banner_orm = models.BannerORM(
                    title=banner.content.title,
                    text=banner.content.text,
                    url=banner.content.url,
                    is_active=banner.is_active,
                    feature_id=banner.feature_id,
                )
                session.add(banner_orm)
                await session.flush()
                return banner_orm.id

    @classmethod
    async def create_tag(cls, tag_name: str = "some_tag_name") -> models.TagORM:
        async with async_session_factory() as session:
            async with session.begin():
                tag_orm = models.TagORM(
                    name=tag_name,
                )
                session.add(tag_orm)
                await session.flush()
                return tag_orm.id

    @classmethod
    async def get_tag_by_id(cls, tag_id: int) -> models.TagORM | None:
        async with async_session_factory() as session:
            async with session.begin():
                tag_orm = await session.execute(
                    select(models.TagORM).filter(models.TagORM.id == tag_id)
                )
                return tag_orm.scalar_one_or_none()

    @classmethod
    async def create_tag_with_id(cls, tag_id: int) -> models.TagORM:
        async with async_session_factory() as session:
            async with session.begin():
                current_tag_max_id = await cls._get_current_tag_max_id()
                if tag_id <= current_tag_max_id:
                    raise ValueError(f"Tag id {tag_id} already exists")
                tags = [
                    models.TagORM(name="some_tag_name") for _ in range(tag_id - current_tag_max_id)
                ]
                session.add_all(tags)
                await session.flush()
                return tags[-1]

    @classmethod
    async def _get_current_tag_max_id(cls) -> int:
        async with async_session_factory() as session:
            async with session.begin():
                tag_max_id = await session.execute(select(func.max(models.TagORM.id)))
                return tag_max_id.scalar() or 0

    @classmethod
    async def get_feature_by_id(cls, feature_id: int) -> models.FeatureORM | None:
        async with async_session_factory() as session:
            async with session.begin():
                feature_orm = await session.execute(
                    select(models.FeatureORM).filter(models.FeatureORM.id == feature_id)
                )
                return feature_orm.scalar_one_or_none()

    @classmethod
    async def _get_current_feature_max_id(cls) -> int:
        async with async_session_factory() as session:
            async with session.begin():
                feature_max_id = await session.execute(select(func.max(models.FeatureORM.id)))
                return feature_max_id.scalar() or 0

    @classmethod
    async def create_feature_with_id(cls, feature_id: int) -> models.FeatureORM:
        async with async_session_factory() as session:
            async with session.begin():
                current_feature_max_id = await cls._get_current_feature_max_id()
                if feature_id <= current_feature_max_id:
                    raise ValueError(f"Feature id {feature_id} already exists")
                features = [
                    models.FeatureORM(name="some_feature_name")
                    for _ in range(feature_id - current_feature_max_id)
                ]
                session.add_all(features)
                await session.flush()
                return features[-1]

    @classmethod
    async def create_relation_banner_tag(cls, banner_id: int, tag_id: int | Iterable[int]) -> None:
        async with async_session_factory() as session:
            async with session.begin():
                if isinstance(tag_id, Iterable):
                    for tag_id_ in tag_id:
                        relation_banner_feature_orm = models.BannerTagORM(
                            banner_id=banner_id,
                            tag_id=tag_id_,
                        )
                        session.add(relation_banner_feature_orm)
                else:
                    relation_banner_feature_orm = models.BannerTagORM(
                        banner_id=banner_id,
                        tag_id=tag_id,
                    )
                    session.add(relation_banner_feature_orm)
                await session.flush()
                return
