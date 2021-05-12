from aiohttp import ClientSession
from dependency_injector import containers, providers
from infrastructure.repositories.proxy_sendler.repository import ProxySend


class ProxySendContainer(containers.DeclarativeContainer):
    aio: ClientSession = providers.Dependency(instance_of=ClientSession)

    configs = providers.Configuration()

    repository = providers.Factory(
        ProxySend, multi_url=configs.api_multi_url, single_url=configs.api_single_url, session=aio
    )
