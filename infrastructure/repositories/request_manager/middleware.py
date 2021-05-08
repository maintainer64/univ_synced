from asyncio import create_task, Future

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from core.any_migration.application.repository import UseCase
from core.proxy_sendler.exceptions import NotResolvedError
from core.proxy_sendler.repository import ProxySendBase
from core.request_manager.dto import RequestManagerDTO


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, proxy: "Future[ProxySendBase]", manager: UseCase[RequestManagerDTO]):
        super().__init__(app)
        self.proxy_send = proxy
        self.manager = manager

    async def dispatch(self, request: Request, call_next):
        try:
            return await self.dispatch_and_proxy(request)
        except NotResolvedError:
            return await call_next(request)

    async def dispatch_and_proxy(self, request: Request):
        proxy_send = self.proxy_send.result()
        response_dto = await proxy_send.proxy(request)
        create_task(self.manager.execute(input_dto=RequestManagerDTO(request=request, response=response_dto,)))
        return Response(content=response_dto.content, status_code=response_dto.status, headers=response_dto.headers,)
