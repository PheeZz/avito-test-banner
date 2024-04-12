import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, RedirectResponse

from customize_logger import CustomizeLogger
from source.api.v1.banner.router import router as banner_router
from source.api.v1.set_header.router import router as set_header_router
from source.middleware import request_process_time_log

logger = logging.getLogger(__name__)

logger_config_path = Path(__file__).with_name("logging_config.json")

app = FastAPI(
    title="KDC CARE API",
    version="0.1.0",
    redoc_url=None,
    docs_url=None,
    openapi_url=None,
)
logger = CustomizeLogger.make_logger(logger_config_path)
app.logger = logger  # type: ignore


app.include_router(banner_router)
app.include_router(set_header_router)
app.add_middleware(middleware_class=request_process_time_log.ProcessTimeLogMiddleware)
app.add_middleware(
    middleware_class=CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Authorization",
        "token",
    ],
)


@app.get("/")
async def root():
    return RedirectResponse(
        url="/docs",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )


@app.get(
    "/docs",
    tags=["documentation"],
    operation_id="get_documentation",
    include_in_schema=False,
)
async def get_swagger_documentation() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get(
    "/openapi.json",
    tags=["documentation"],
    operation_id="get_openapi_json",
    include_in_schema=False,
)
async def openapi() -> dict[str, Any]:
    return get_openapi(
        title="Avito banner API",
        servers=[
            {"url": "http://127.0.0.1:8000", "description": "Local DEV server"},
        ],
        version="0.1.0",
        routes=app.routes,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1:8000", port=8000)
