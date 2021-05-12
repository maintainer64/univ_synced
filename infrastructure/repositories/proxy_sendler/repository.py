import logging
from json import JSONDecodeError
from typing import Optional, List, Tuple

from aiohttp import ClientSession, ClientResponse
from starlette.datastructures import URL
from starlette.requests import Request

from core.proxy_sendler.entities import ResolverEntity, ResponseProxyDTO
from core.proxy_sendler.exceptions import NotResolvedError
from core.proxy_sendler.repository import ProxySendBase

logger = logging.getLogger(__name__)


class ProxySend(ProxySendBase):
    def __init__(self, multi_url: str, single_url: str, session: ClientSession):
        allow_headers_request = ["user-agent"]
        allow_headers_response = ["Content-Type"]
        self._resolver = (
            ResolverEntity(
                base_url=multi_url,
                prefix_path="/multi/",
                allow_headers_request=allow_headers_request,
                allow_headers_response=allow_headers_response,
            ),
            ResolverEntity(
                base_url=single_url,
                prefix_path="/single/",
                allow_headers_request=allow_headers_request,
                allow_headers_response=allow_headers_response,
            ),
        )
        self.multi_url = multi_url
        self.single_url = single_url
        self.session = session

    @staticmethod
    def prepare_header(headers: dict, allow_headers: Optional[List[str]]) -> dict:
        if allow_headers is None:
            return headers
        allow_headers_data = dict()
        for header_str in allow_headers:
            if headers.get(header_str) is not None:
                allow_headers_data[header_str] = headers.get(header_str)
        return allow_headers_data

    async def proxy(self, request: Request) -> ResponseProxyDTO:
        try:
            json = await request.json()
        except JSONDecodeError:
            json = None
        new_url, resolver_entity = await self.resolve_url(url=request.url)
        logger.info(f"Proxy from {request.url} to {new_url} by {request.method}")
        response = await self.session.request(
            method=request.method,
            url=new_url,
            params=request.query_params,
            json=json,
            cookies=request.cookies,
            headers=self.prepare_header(headers=request.headers, allow_headers=resolver_entity.allow_headers_request),
            raise_for_status=False,
        )
        return await self._convert_response_to_dto(response=response, resolver=resolver_entity)

    @staticmethod
    def _check_and_rewrite(url: URL, resolve: ResolverEntity) -> Optional[str]:
        if url.path.startswith(resolve.prefix_path):
            rewrite_path = url.path.lstrip(resolve.prefix_path)
            return resolve.base_url.strip("/") + "/" + rewrite_path
        return None

    async def _convert_response_to_dto(self, response: ClientResponse, resolver: ResolverEntity) -> ResponseProxyDTO:
        content = await response.read()
        return ResponseProxyDTO(
            content=content,
            headers=self.prepare_header(headers=response.headers, allow_headers=resolver.allow_headers_response),
            status=response.status,
            url=str(response.url),
        )

    async def resolve_url(self, url: URL) -> Tuple[str, ResolverEntity]:
        for resolve in self._resolver:
            rewrite_path = self._check_and_rewrite(url=url, resolve=resolve)
            if rewrite_path is not None:
                return rewrite_path, resolve
        raise NotResolvedError
