from fastapi import HTTPException, status


class ErrorBannerNotActive(HTTPException):
    def __init__(self, banner_id: int):
        detail = f"Баннер {banner_id} не активен"
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
    def __init__(self, banner_id: int):
        detail = f"Баннер {banner_id} не найден"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
