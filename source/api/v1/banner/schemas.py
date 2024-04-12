from pydantic import BaseModel, Field, field_validator


class ContentSchema(BaseModel):
    title: str = Field(
        title="Заголовок баннера",
        max_length=255,
        examples=["Скидка 50% на все товары"],
    )
    text: str = Field(
        title="Текст баннера",
        max_length=2000,
        examples=["Только до конца недели..."],
    )
    url: str = Field(
        title="Ссылка на страницу с подробным описанием",
        max_length=500,
        examples=["https://example.com/sale"],
        pattern=r"https?://",
    )


class CreateBannerSchema(BaseModel):
    tag_ids: list[int] = Field(
        title="Идентификаторы тегов",
        description=(
            "Список идентификаторов тегов,"
            "к которым относится баннер, каждое значение должно быть больше 0"
        ),
        examples=[[1, 2, 3]],
    )
    feature_id: int = Field(
        title="Идентификатор фичи",
        examples=[1],
        gt=0,
    )
    content: ContentSchema = Field(
        title="Содержимое баннера",
    )
    is_active: bool = Field(
        title="Активность баннера",
        examples=[True],
    )

    @field_validator("tag_ids")
    def check_tags_ids(cls, v):
        if not v:
            raise ValueError("tag_ids не может быть пустым")
        for tag_id in v:
            if tag_id <= 0:
                raise ValueError("каждый tag_id должен быть больше 0")
        return v


class BannerSuccessfullyCreatedSchema(BaseModel):
    """Code: 201"""

    banner_id: int = Field(
        title="Идентификатор созданного баннера",
        examples=[1],
        gt=0,
    )


class ErrorBannerNotActiveSchema(BaseModel):
    """Code: 400"""

    detail: str = Field(
        title="Сообщение об ошибке",
        description="Баннер не активен",
        examples=["Баннер не активен"],
    )


class ErrorUserNotAuthorizedSchema(BaseModel):
    """Code: 401"""

    detail: str = Field(
        title="Сообщение об ошибке",
        description="Пользователь не авторизован",
        examples=["Пользователь не авторизован"],
    )


class ErrorUserHaveNoAccessSchema(BaseModel):
    """Code: 403"""

    detail: str = Field(
        title="Сообщение об ошибке",
        description="Пользователь не имеет доступа",
        examples=["Пользователь не имеет доступа"],
    )


class ErrorBannerNotFoundSchema(BaseModel):
    """Code: 404"""

    detail: str = Field(
        title="Сообщение об ошибке",
        description="Баннер не найден",
        examples=["Баннер не найден"],
    )


class InternalErrorSchema(BaseModel):
    """Code: 500"""

    detail: str = Field(
        title="Сообщение об ошибке",
        description="Внутренняя ошибка сервера",
        examples=["Внутренняя ошибка сервера"],
    )
