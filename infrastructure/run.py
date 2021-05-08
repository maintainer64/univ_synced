from starlette.applications import Starlette
from starlette.middleware import Middleware
from infrastructure.repositories.request_manager.middleware import CustomHeaderMiddleware


def get_app():
    from infrastructure.command.utils import get_inject_dependency

    di = get_inject_dependency()

    from infrastructure.dependencies.dependencies_function import get_proxy
    from infrastructure.repositories.request_manager import router

    _app = Starlette(debug=True, middleware=[Middleware(CustomHeaderMiddleware, proxy=get_proxy(), manager=router)])
    _app.state.container = di
    return _app


app = get_app()
