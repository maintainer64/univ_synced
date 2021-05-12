import logging
from typing import List

import orjson
from starlette.responses import Response
from starlette.routing import Route

from core.any_migration.application.repository import UseCase
from core.request_manager.dto import RequestManagerDTO
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class RequestApplicationManager(UseCase[RequestManagerDTO]):
    def __init__(self):
        self._router: List[Route] = []

    @staticmethod
    def _create_decorator_function(func, val: BaseModel):
        """
        Создаём декоратор, который запускается при запросе
        :param func: Функция, которая отработает, если пришёл нужный параметр
        :param val: Вылидация в query-params
        :return:
        """

        async def execute(input_dto: RequestManagerDTO):
            if input_dto.request.method == "GET":
                return Response(content=None, status_code=500)

            try:
                json_data = orjson.loads(input_dto.response.content)
            except orjson.JSONDecodeError:
                json_data = None

            try:
                validate_data = val.parse_obj(dict(query=input_dto.request.query_params, data=json_data))
                await func(request=validate_data)
            except ValidationError as err:
                logger.exception(
                    "ValidationError data from manager",
                    extra={"error": err, "request": {"url": input_dto.request.url, "method": input_dto.request.method}},
                )
                return Response(content=None, status_code=500)
            return Response(content=None, status_code=200)

        return execute

    def route(self, path, val=None, methods=None):
        """
        Декоратор, для создания контекста функции и добавления в router
        :param path: url для отработки метода
        :param val: BaseModel
        :param methods: Разрешённые методы для API
        :return:
        """

        def wrapper(func):
            endpoint = self._create_decorator_function(func=func, val=val,)
            self._router.append(Route(path=path, endpoint=endpoint, methods=methods))
            return func

        return wrapper

    async def execute(self, input_dto: RequestManagerDTO):
        for route in self._router:
            path, method = input_dto.request.url.path, input_dto.request.method
            if path == route.path and method in route.methods:
                logger.info(f"Hook execute {method} {path}")
                await route.endpoint(input_dto)
