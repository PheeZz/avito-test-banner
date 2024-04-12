import logging
from typing import Annotated

from fastapi import Header

from source.api.v1.set_header.constants import ADMIN_TOKEN, USER_TOKEN

from . import schemas
from .dao import BannerDAO
from .exceptions import ErrorUserHaveNoAccess, ErrorUserNotAuthorized

logger = logging.getLogger(__name__)


def check_admin_token_header(token: Annotated[str | None, Header()] = None):
    check_user_authorized(token)
    if token != ADMIN_TOKEN:
        raise ErrorUserHaveNoAccess


def check_user_token_header(token: Annotated[str | None, Header()] = None):
    check_user_authorized(token)
    # if token != USER_TOKEN:
    #     raise ErrorUserHaveNoAccess


def check_user_authorized(token: Annotated[str | None, Header()] = None):
    if token is None:
        raise ErrorUserNotAuthorized


async def add_tags_if_not_exist(banner: schemas.CreateBannerSchema):
    tag_max_id = max(banner.tag_ids)
    try:
        await BannerDAO.create_tag_with_id(tag_max_id)
    except ValueError as e:
        logger.info(f"{e.__class__.__name__}: {e}")


async def add_feature_if_not_exist(banner: schemas.CreateBannerSchema):
    try:
        await BannerDAO.create_feature_with_id(banner.feature_id)
    except ValueError as e:
        logger.info(f"{e.__class__.__name__}: {e}")
