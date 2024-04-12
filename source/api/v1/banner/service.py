from . import schemas
from .dao import BannerDAO


async def create_banner(banner: schemas.CreateBannerSchema) -> int:
    banner_id = await BannerDAO.create_banner(banner)
    await BannerDAO.create_relation_banner_tag(banner_id, banner.tag_ids)
    return banner_id
