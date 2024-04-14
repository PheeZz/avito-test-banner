from fastapi import HTTPException, status


class ErrorBannerNotActive(HTTPException):
    def __init__(self, banner_id: int):
        detail = f"Баннер {banner_id} не активен"
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class ErrorTagAndFeatureRelationAlreadyExist(HTTPException):

    def __init__(self, feature_id: int, tag_id: int, banner_id: int):
        detail = (
            f"Отношение между фичей {feature_id} и тегом(-ами) {tag_id} уже существует."
            f"banner_id: {banner_id}"
        )
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class ErrorUserNotAuthorized(HTTPException):
    def __init__(self):
        detail = "Пользователь не авторизован"
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class ErrorUserHaveNoAccess(HTTPException):
    def __init__(self):
        detail = "Пользователь не имеет доступа"
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class ErrorBannerNotFound(HTTPException):
    def __init__(
        self, banner_id: int | None = None, feature_id: int | None = None, tag_id: int | None = None
    ):
        if feature_id and tag_id:
            detail = f"Баннер не найден по тегу {tag_id} и фиче {feature_id}"
        elif banner_id:
            detail = f"Баннер {banner_id} не найден"
        else:
            detail = "Баннер не найден"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ErrorValueMustBeGTEZero(HTTPException):
    def __init__(self, value: int, field: str):
        detail = f"Значение {field} должно быть не меньше 0. Передано: {value}"
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class ErrorNoFeatureOrTagIdProvided(HTTPException):
    def __init__(self):
        detail = (
            "Не переданы идентификаторы фичи или тега. Хотя бы один параметр должен быть передан"
        )
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
