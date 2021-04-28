import dataclasses
import logging
import typing
from abc import ABC
from typing import Optional
from urllib.parse import urljoin

import orjson
from aiohttp import ClientResponse, ClientSession, ContentTypeError

from infrastructure.repositories.client_template.exceptions import ApiErrorBase

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class ApiRepository(ABC):
    base_url: str
    session: ClientSession
    token: Optional[str] = None

    async def handle_response(self, response: ClientResponse) -> typing.Optional[typing.Dict]:
        try:
            response = await response.json(loads=orjson.loads)
        except ContentTypeError as err:
            logger.exception("ApiErrorWithClient", extra={"error": err, "base_url": self.base_url})
            raise ApiErrorBase(code=-6000, message=err.message, meta={"status": response.status})
        return response

    async def _request(
        self,
        method: str,
        path: typing.Optional[str] = None,
        no_response: bool = False,
        **params,
    ) -> typing.Any:
        """Выполнить запрос.

        Args:
            method: HTTP метод (GET, POST, PUT, DELETE, HEAD...)
            path: Полная ссылка или часть пути до ресурса
            **params: Параметры запроса

        Returns:
            Ответ на запрос
        :raise: ValueError, ApiErrorBase
        :return: Dict
        """
        if self.base_url is None and path is None:
            raise ValueError("Должн быть заполнет хотя бы один из параметров base_url или path")

        full_url = urljoin(self.base_url, path)

        logger.info(f"Запрос {method} на {full_url}\n параметры {params}")

        response = await self.session.request(method=method, url=full_url, raise_for_status=True, **params)
        if not no_response:
            result = await self.handle_response(response=response)
            return result
