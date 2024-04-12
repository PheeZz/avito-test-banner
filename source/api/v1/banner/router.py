from typing import Annotated

from fastapi import APIRouter, Depends, Header, Response, status

from . import dependencies, exceptions, schemas, service

router = APIRouter(tags=["Banner"])


@router.get(
    "/user_banner",
    name="Получение баннера для пользователя",
)
async def get_user_banner(
    tag_id: int,
    feature_id: int,
    use_last_revision: bool = False,
    token: Annotated[str | None, Header()] = None,  # user token
): ...


@router.get(
    "/banner",
    name="Получение всех баннеров с фильтрацией по фиче и/или тегу",
)
async def get_banner(
    token: Annotated[str | None, Header()] = None,  # admin token
    feature_id: int = None,
    tag_id: int = None,
    limit: int = 10,
    offset: int = 0,
): ...


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
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Пользователь не авторизован",
            "model": schemas.ErrorUserNotAuthorizedSchema,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Пользователь не имеет доступа",
            "model": schemas.ErrorUserHaveNoAccessSchema,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера",
            "model": schemas.InternalErrorSchema,
        },
    },
    dependencies=[
        Depends(dependencies.add_tags_if_not_exist),
        Depends(dependencies.add_feature_if_not_exist),
        Depends(dependencies.check_admin_token_header),
    ],
)
async def post_new_banner(
    banner: schemas.CreateBannerSchema,
):
    """
    Допустимо использование только с админским токеном
    """
    banner_id = await service.create_banner(banner)
    return schemas.BannerSuccessfullyCreatedSchema(banner_id=banner_id)


@router.patch(
    "/banner/{id}",
    name="Обновление содержимого баннера",
)
async def patch_banner(
    banner: schemas.CreateBannerSchema,
    token=Depends(dependencies.check_admin_token_header),  # admin token,
): ...


@router.delete(
    "/banner/{id}",
    name="Удаление баннера по идентификатору",
)
async def delete_banner(
    id: int,
    token=Depends(dependencies.check_admin_token_header),  # admin token,
): ...
