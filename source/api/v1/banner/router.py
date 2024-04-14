from typing import Literal

from fastapi import APIRouter, Depends, status

from . import dependencies, schemas, service
from .constants import INTERNAL_SERVER_ERROR_SWAGGER_RESPONSE

router = APIRouter(tags=["Banner"])


@router.get(
    "/user_banner",
    name="Получение баннера для пользователя",
    response_model=schemas.ContentSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(dependencies.check_user_token_header),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Пользователь не авторизован",
            "model": schemas.ErrorUserNotAuthorizedSchema,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Пользователь не имеет доступа",
            "model": schemas.ErrorUserHaveNoAccessSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Баннер не найден",
            "model": schemas.ErrorBannerNotFoundSchema,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR_SWAGGER_RESPONSE,
    },
)
async def get_user_banner(
    tag_id: int,
    feature_id: int,
    use_last_revision: bool = False,
    user_type: Literal["admin", "user"] = Depends(dependencies.get_user_type_by_token),
):
    if not use_last_revision:
        banner = await service.get_cached_user_banner(
            tag_id=tag_id,
            feature_id=feature_id,
            user_type=user_type,
        )
    else:
        banner = await service.get_user_banner(
            tag_id=tag_id,
            feature_id=feature_id,
            user_type=user_type,
        )
    return schemas.ContentSchema(
        title=banner.title,
        text=banner.text,
        url=banner.url,
    )


@router.get(
    "/banner",
    name="Получение всех баннеров с фильтрацией по фиче и/или тегу",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.BannerFullInfoSchema],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Значение должно быть не меньше 0",
            "model": schemas.ErrorValueMustBeGTEZeroSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Пользователь не авторизован",
            "model": schemas.ErrorUserNotAuthorizedSchema,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Пользователь не имеет доступа",
            "model": schemas.ErrorUserHaveNoAccessSchema,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR_SWAGGER_RESPONSE,
    },
    dependencies=[
        Depends(dependencies.check_admin_token_header),
    ],
)
async def get_banner(
    feature_id: int = None,
    tag_id: int = None,
    limit: int = Depends(dependencies.check_limit_gt_zero),
    offset: int = Depends(dependencies.check_offset_gte_zero),
):
    banners = await service.get_banners(
        feature_id=feature_id,
        tag_id=tag_id,
        limit=limit,
        offset=offset,
    )
    if not banners:
        return []
    return [schemas.BannerFullInfoSchema(**banner) for banner in banners]


@router.post(
    "/banner",
    name="Создание нового баннера",
    response_model=schemas.BannerSuccessfullyCreatedSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Баннер успешно создан",
            "model": schemas.BannerSuccessfullyCreatedSchema,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Нарушение уникальности отношения фичи и тега",
            "model": schemas.ErrorTagAndFeatureRelationAlreadyExistSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Пользователь не авторизован",
            "model": schemas.ErrorUserNotAuthorizedSchema,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Пользователь не имеет доступа",
            "model": schemas.ErrorUserHaveNoAccessSchema,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR_SWAGGER_RESPONSE,
    },
    dependencies=[
        Depends(dependencies.check_feat_and_tag_ids_not_violate_rules),
        Depends(dependencies.add_tags_if_not_exist),
        Depends(dependencies.add_feature_if_not_exist),
        Depends(dependencies.check_admin_token_header),
    ],
)
async def post_new_banner(
    banner: schemas.CreateUpdateBannerSchema,
):
    """
    Допустимо использование только с админским токеном
    """
    banner_id = await service.create_banner(banner)
    return schemas.BannerSuccessfullyCreatedSchema(banner_id=banner_id)


@router.patch(
    "/banner/{id}",
    name="Обновление содержимого баннера",
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(dependencies.add_tags_if_not_exist),
        Depends(dependencies.add_feature_if_not_exist),
        Depends(dependencies.check_admin_token_header),
    ],
    responses={
        status.HTTP_200_OK: {
            "description": "Баннер успешно обновлен",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Пользователь не авторизован",
            "model": schemas.ErrorUserNotAuthorizedSchema,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Пользователь не имеет доступа",
            "model": schemas.ErrorUserHaveNoAccessSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Баннер не найден",
            "model": schemas.ErrorBannerNotFoundSchema,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR_SWAGGER_RESPONSE,
    },
)
async def patch_banner(
    banner: schemas.CreateUpdateBannerSchema,
    banner_orm=Depends(dependencies.get_banner_by_id),
):
    """
    Допустимо использование только с админским токеном
    """
    await service.update_banner(
        banner_orm=banner_orm,
        banner=banner,
    )


@router.delete(
    "/banner/{id}",
    name="Удаление баннера по идентификатору",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(dependencies.check_admin_token_header),
    ],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Баннер успешно удален",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Пользователь не авторизован",
            "model": schemas.ErrorUserNotAuthorizedSchema,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Пользователь не имеет доступа",
            "model": schemas.ErrorUserHaveNoAccessSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Баннер не найден",
            "model": schemas.ErrorBannerNotFoundSchema,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR_SWAGGER_RESPONSE,
    },
)
async def delete_banner(
    banner_orm=Depends(dependencies.get_banner_by_id),
) -> None:
    """
    Допустимо использование только с админским токеном
    """
    await service.delete_banner(banner_orm=banner_orm)


@router.delete(
    "/banner/",
    name="Удаление баннера по feature_id и/или tag_id",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(dependencies.check_admin_token_header),
    ],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Баннер(ы) успешно удален(ы)",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Не переданы идентификаторы фичи или тега.",
            "model": schemas.ErrorNoFeatureOrTagIdProvidedSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Пользователь не авторизован",
            "model": schemas.ErrorUserNotAuthorizedSchema,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Пользователь не имеет доступа",
            "model": schemas.ErrorUserHaveNoAccessSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Баннер не найден",
            "model": schemas.ErrorBannerNotFoundSchema,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера",
            "content": {
                "text/plain": {
                    "example": "Internal Server Error",
                },
            },
        },
    },
)
async def delete_banner_by_feat_or_tag_id(
    feature_id: int = None,
    tag_id: int = None,
):
    """
    Допустимо использование только с админским токеном
    """
    await service.delete_banners_by_feat_or_tag_id(
        feature_id=feature_id,
        tag_id=tag_id,
    )
    return None
