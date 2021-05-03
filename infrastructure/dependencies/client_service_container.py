from aiohttp import ClientSession
from dependency_injector import containers, providers

from infrastructure.repositories.multitable_api.repository import MultitableUniversityApi
from infrastructure.repositories.singletable_api.repository import SingletableUniversityApi


class ServiceClientContainer(containers.DeclarativeContainer):
    aio: ClientSession = providers.Dependency(instance_of=ClientSession)

    configs = providers.Configuration()

    multi = providers.Factory(
        MultitableUniversityApi,
        base_url=configs.api_multi_url,
        session=aio,
    )
    single = providers.Factory(
        SingletableUniversityApi,
        base_url=configs.api_single_url,
        session=aio,
    )
