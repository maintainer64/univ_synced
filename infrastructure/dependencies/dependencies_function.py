from core.proxy_sendler.repository import ProxySendBase
from dependency_injector.wiring import inject, Provide

from infrastructure.dependencies.application_container import ApplicationDependenciesContainer as DD


@inject
def get_proxy(proxy: ProxySendBase = Provide[DD.proxy_sendler.repository]):
    return proxy
