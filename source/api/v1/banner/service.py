from datetime import datetime
from typing import Literal

from fastapi_cache.decorator import cache

from . import models, schemas
from .dao import BannerDAO
from .exceptions import ErrorBannerNotActive, ErrorBannerNotFound


async def create_banner(banner: schemas.CreateUpdateBannerSchema) -> int:
    banner_id = await BannerDAO.create_banner(banner)
    await BannerDAO.create_relation_banner_tag(banner_id, banner.tag_ids)
    return banner_id


async def delete_banner(banner_orm: models.BannerORM) -> None:
    await BannerDAO.delete_banner(banner_orm)


async def update_banner(
    banner_orm: models.BannerORM, banner: schemas.CreateUpdateBannerSchema
) -> None:
    await BannerDAO.update_banner(banner_orm, banner)
    await BannerDAO.update_relation_banner_tag(banner_orm.id, banner.tag_ids)


async def get_user_banner(
    tag_id: int, feature_id: int, user_type: Literal["admin", "user"]
) -> models.BannerORM:
    banner_orm = await BannerDAO.get_banner_by_tag_and_feature(tag_id, feature_id)
    if not banner_orm:
        raise ErrorBannerNotFound(tag_id=tag_id, feature_id=feature_id)
    if not banner_orm.active and user_type == "user":
        raise ErrorBannerNotActive(banner_id=banner_orm.id)

    return banner_orm


@cache(expire=300)
async def get_cached_user_banner(
    tag_id: int, feature_id: int, user_type: Literal["admin", "user"]
) -> models.BannerORM:
    return await get_user_banner(tag_id, feature_id, user_type)


async def get_banners(
    tag_id: int | None, feature_id: int | None, limit: int, offset: int
) -> list[dict[str, str | int | bool | datetime]]:
    full_banners_info = await BannerDAO.get_banners(tag_id, feature_id, limit, offset)
    if not full_banners_info:
        return []
    return [
        {
            "banner_id": banner["id"],
            "content": {
                "title": banner["title"],
                "text": banner["text"],
                "url": banner["url"],
            },
            "active": banner["active"],
            "created_at": banner["created_at"],
            "updated_at": banner["updated_at"],
            "tag_ids": banner["tag_ids"],
            "feature_id": banner["feature_id"],
        }
        for banner in full_banners_info
    ]
