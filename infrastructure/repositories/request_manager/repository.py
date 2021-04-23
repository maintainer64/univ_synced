from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route


class RequestApplicationManager:
    def __init__(self):
        self._router = []

    @staticmethod
    def _create_decorator_function(func, name_identifier):
        """
        Создаём декоратор, который запускается при запросе
        :param func: Функция, которая отработает, если пришёл нужный параметр
        :param name_identifier: Параметр, который ожидается в query_params
        :return:
        """

        async def execute(request: Request):
            if request.method == "GET":
                return Response(content=None, status_code=500)
            param = request.query_params.get(name_identifier)
            if request.query_params.get(name_identifier) is None:
                return Response(content=None, status_code=500)
            await func(param)
            return Response(content=None, status_code=200)

        return execute

    def route(self, path, name_identifier):
        """
        Декоратор, для создания контекста функции и добавления в router
        :param path: url для отработки метода
        :param name_identifier: параметр из query_params
        :return:
        """

        def wrapper(func):
            endpoint = self._create_decorator_function(func=func, name_identifier=name_identifier,)
            self._router.append(Route(path=path, endpoint=endpoint, methods=["POST", "PUT"]))
            return func

        return wrapper

    def get_server(self) -> Starlette:
        return Starlette(debug=True, routes=self._router)
