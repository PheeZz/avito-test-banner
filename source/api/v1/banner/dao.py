from datetime import datetime
from logging import getLogger
from typing import Iterable

from sqlalchemy import delete, func, select
from sqlalchemy.orm import aliased

from source.database import async_session_factory

from . import models, schemas

logger = getLogger(__name__)


class BannerDAO:
    @classmethod
    async def create_banner(cls, banner: schemas.CreateUpdateBannerSchema) -> int:
        async with async_session_factory() as session:
            async with session.begin():
                banner_orm = models.BannerORM(
                    title=banner.content.title,
                    text=banner.content.text,
                    url=banner.content.url,
                    active=banner.active,
                    feature_id=banner.feature_id,
                )
                session.add(banner_orm)
                await session.flush()
                return banner_orm.id

    @classmethod
    async def get_banner_by_id(cls, banner_id: int) -> models.BannerORM | None:
        async with async_session_factory() as session:
            async with session.begin():
                banner_orm = await session.execute(
                    select(models.BannerORM).filter(models.BannerORM.id == banner_id)
                )
                return banner_orm.scalar_one_or_none()

    @classmethod
    async def get_banners(
        cls, tag_id: int | None, feature_id: int | None, limit: int, offset: int
    ) -> list[dict[str, str | int | bool | datetime]] | None:
        async with async_session_factory() as session:
            async with session.begin():
                b = aliased(models.BannerORM)
                bt = aliased(models.BannerTagORM)

                query = (
                    select(b, bt)
                    .join(bt, b.id == bt.banner_id)
                    .filter(b.feature_id == feature_id if feature_id else True)
                    .filter(bt.tag_id == tag_id if tag_id else True)
                    .limit(limit)
                    .offset(offset)
                )

                unsorted_data = await session.execute(query)
                unsorted_data = unsorted_data.all()
                if not unsorted_data:
                    return None
                sorted_data = []

                for banner, banner_tag in unsorted_data:
                    for sorted_banner in sorted_data:
                        if sorted_banner["id"] == banner_tag.banner_id:
                            sorted_banner["tag_ids"].append(banner_tag.tag_id)
                            break
                    else:
                        sorted_data.append(
                            {
                                "id": banner.id,
                                "title": banner.title,
                                "text": banner.text,
                                "url": banner.url,
                                "active": banner.active,
                                "created_at": banner.created_at,
                                "updated_at": banner.updated_at,
                                "tag_ids": [banner_tag.tag_id],
                                "feature_id": banner.feature_id,
                            }
                        )
                return sorted_data

    @classmethod
    async def get_banner_by_tag_and_feature(
        cls, feature_id: int, tag_id: int
    ) -> models.BannerORM | None:
        async with async_session_factory() as session:
            async with session.begin():
                b = aliased(models.BannerORM)
                bt = aliased(models.BannerTagORM)

                query = (
                    select(b)
                    .join(bt, b.id == bt.banner_id)
                    .filter(b.feature_id == feature_id)
                    .filter(bt.tag_id == tag_id)
                )

                banner_orm = await session.execute(query)
                banner_orm = banner_orm.scalar_one_or_none()
                session.expunge(banner_orm)

                return banner_orm

    @classmethod
    async def update_banner(
        banner_orm: models.BannerORM, banner: schemas.CreateUpdateBannerSchema
    ) -> None:
        async with async_session_factory() as session:
            async with session.begin():
                banner_orm.title = banner.content.title
                banner_orm.text = banner.content.text
                banner_orm.url = banner.content.url
                banner_orm.active = banner.active
                banner_orm.feature_id = banner.feature_id
                await session.flush()
                return

    @classmethod
    async def delete_banner(cls, banner_orm: models.BannerORM) -> None:
        async with async_session_factory() as session:
            async with session.begin():
                await session.delete(banner_orm)
                await session.flush()
                return

    @classmethod
    async def delete_banners_by_feat_or_tag_id(
        cls, feature_id: int | None, tag_id: int | None
    ) -> None:
        async with async_session_factory() as session:
            async with session.begin():
                b = aliased(models.BannerORM)
                bt = aliased(models.BannerTagORM)

                query = (
                    select(b)
                    .join(bt, b.id == bt.banner_id)
                    .filter(b.feature_id == feature_id if feature_id else True)
                    .filter(bt.tag_id == tag_id if tag_id else True)
                )

                res = await session.execute(query)
                banners = res.scalars().all()
                for banner in banners:
                    await session.delete(banner)
                await session.flush()
                return

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
    async def create_tag_with_id(cls, tag_id: int) -> int:
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
                return tags[-1].id

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

    @classmethod
    async def update_relation_banner_tag(
        cls,
        banner_orm: models.BannerORM,
        tag_id: int | Iterable[int],
    ) -> None:
        async with async_session_factory() as session:
            async with session.begin():
                await session.execute(
                    delete(models.BannerTagORM).filter(
                        models.BannerTagORM.banner_id == banner_orm.id
                    )
                )
                await session.flush()
                await cls.create_relation_banner_tag(banner_orm.id, tag_id)
                return
