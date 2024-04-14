import logging
from typing import Annotated, Literal

from fastapi import Header

from source.api.v1.set_header.constants import ADMIN_TOKEN

from . import models, schemas
from .dao import BannerDAO
from .exceptions import (
    ErrorBannerNotFound,
    ErrorUserHaveNoAccess,
    ErrorUserNotAuthorized,
    ErrorValueMustBeGTEZero,
)

logger = logging.getLogger(__name__)


def check_admin_token_header(token: Annotated[str | None, Header()] = None):
    check_user_authorized(token)
    if token != ADMIN_TOKEN:
        raise ErrorUserHaveNoAccess


def check_user_token_header(token: Annotated[str | None, Header()] = None):
    check_user_authorized(token)


def check_user_authorized(token: Annotated[str | None, Header()] = None):
    if token is None:
        raise ErrorUserNotAuthorized


async def add_tags_if_not_exist(banner: schemas.CreateUpdateBannerSchema):
    tag_max_id = max(banner.tag_ids)
    try:
        await BannerDAO.create_tag_with_id(tag_max_id)
    except ValueError as e:
        logger.info(f"{e.__class__.__name__}: {e}")


async def add_feature_if_not_exist(banner: schemas.CreateUpdateBannerSchema):
    try:
        await BannerDAO.create_feature_with_id(banner.feature_id)
    except ValueError as e:
        logger.info(f"{e.__class__.__name__}: {e}")


async def get_banner_by_id(id: int) -> models.BannerORM:
    banner_orm = await BannerDAO.get_banner_by_id(banner_id=id)
    if not banner_orm:
        raise ErrorBannerNotFound(banner_id=id)
    return banner_orm


def get_user_type_by_token(
    token: Annotated[str | None, Header()] = None
) -> Literal["admin", "user"]:
    if token == ADMIN_TOKEN:
        return "admin"
    else:
        return "user"


def check_offset_gte_zero(offset: int = 0) -> int:
    if offset < 0:
        raise ErrorValueMustBeGTEZero(value=offset, field="offset")
    return offset


def check_limit_gt_zero(limit: int = 10) -> int:
    if limit < 0:
        raise ErrorValueMustBeGTEZero(value=limit, field="limit")
    return limit
