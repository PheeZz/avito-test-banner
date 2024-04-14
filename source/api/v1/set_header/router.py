from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from . import constants

router = APIRouter(prefix="/set_header_token", tags=["Set header token"])


@router.get(
    "/admin",
    name="Установка токена админа",
    responses={
        200: {
            "description": "Токен АДМИНИСТРАТОРА содержится в headers",
            "content": {
                "application/json": {
                    "example": {"message": "Токен АДМИНИСТРАТОРА содержится в headers"}
                }
            },
            "headers": {
                "token": {
                    "description": "Токен администратора",
                    "type": "string",
                }
            },
        }
    },
)
async def get_admin_token():
    header = {"token": constants.ADMIN_TOKEN}
    return JSONResponse(
        content={"message": "Токен АДМИНИСТРАТОРА содержится в headers"},
        headers=header,
        status_code=status.HTTP_200_OK,
    )
