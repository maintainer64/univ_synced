from abc import ABC, abstractmethod
from starlette.requests import Request
from starlette.datastructures import URL

from core.proxy_sendler.entities import ResponseProxyDTO


class ProxySendBase(ABC):
    @abstractmethod
    async def proxy(self, request: Request) -> ResponseProxyDTO:
        """
        :raises: NotResolvedError
        """
        ...

    @abstractmethod
    async def resolve_url(self, path: URL) -> URL:
        """
        :raises: NotResolvedError
        """
        ...
