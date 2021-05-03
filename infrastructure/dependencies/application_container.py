from dependency_injector import containers, providers

from infrastructure.dependencies.client_service_container import ServiceClientContainer
from infrastructure.dependencies.many_to_one_migration_container import (
    ManyToOneMigrationContainer,
    ManyToOneMigrationUseCasesContainer,
)
from infrastructure.dependencies.utils import session_maker


class ApplicationDependenciesContainer(containers.DeclarativeContainer):
    aio = providers.Resource(session_maker)
    configs = providers.Configuration()
    clients = providers.Container(ServiceClientContainer, aio=aio, configs=configs)
    migration_service_many_to_one = providers.Container(ManyToOneMigrationContainer, clients_repository=clients)
    migration_service_many_to_one_use_cases = providers.Container(
        ManyToOneMigrationUseCasesContainer, migration=migration_service_many_to_one
    )
