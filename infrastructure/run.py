from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from infrastructure.repositories.request_manager.middleware import CustomHeaderMiddleware
from infrastructure.settings import application as conf


def get_app():
    from infrastructure.command.utils import get_inject_dependency

    di = get_inject_dependency()

    from infrastructure.dependencies.dependencies_function import get_proxy
    from infrastructure.repositories.request_manager import router

    _app = Starlette(
        debug=True,
        routes=[Mount("/static", app=StaticFiles(directory=conf.STATIC_DIRECTORY), name="static")],
        middleware=[Middleware(CustomHeaderMiddleware, proxy=get_proxy(), manager=router)],
    )
    _app.state.container = di
    return _app


app = get_app()
