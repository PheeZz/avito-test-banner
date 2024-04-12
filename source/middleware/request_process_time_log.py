import random
import string
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class ProcessTimeLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        req_uid = "".join(random.choices(string.ascii_uppercase + string.digits, k=16))
        start_time = time.time()
        # request_body = await request.body()
        request_params = request.query_params
        request.app.logger.info(
            f"Request {req_uid} for operation {request.url.path}"
            f" received from IP {request.client.host}"
            # f"{'with body ' + json.loads(request_body) if request_body else ''}"
            f"{'with params ' + str(request_params) if request_params else ''}"
        )
        response = await call_next(request)
        time_spent = f"{(time.time() - start_time):0.3f} seconds"
        request.app.logger.info(
            f"Request {req_uid} for operation {request.url.path}"
            f" completed from IP {request.client.host} in {time_spent}"
        )
        return response
