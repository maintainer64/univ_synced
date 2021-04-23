from dependency_injector import containers, providers

from infrastructure.dependencies.client_service_container import ServiceClientContainer
from infrastructure.dependencies.many_to_one_migration_container import (
    ManyToOneMigrationContainer,
    ManyToOneMigrationUseCasesContainer,
)
from infrastructure.dependencies.multi_facade_container import MultiFacadeContainer
from infrastructure.dependencies.one_to_many_migration_container import OneToManyMigrationContainer
from infrastructure.dependencies.tree_single_entity_container import TreeRelatedSingleEntityContainer
from infrastructure.dependencies.utils import session_maker


class ApplicationDependenciesContainer(containers.DeclarativeContainer):
    aio = providers.Resource(session_maker)
    configs = providers.Configuration()
    clients = providers.Container(ServiceClientContainer, aio=aio, configs=configs)
    migration_service_many_to_one = providers.Container(ManyToOneMigrationContainer, clients_repository=clients)
    migration_service_many_to_one_use_cases = providers.Container(
        ManyToOneMigrationUseCasesContainer, migration=migration_service_many_to_one
    )
    tree_single_entity_related = providers.Container(TreeRelatedSingleEntityContainer, clients_repository=clients)
    multi_facade = providers.Container(
        MultiFacadeContainer, single_related=tree_single_entity_related, clients_repository=clients
    )
    migration_service_one_to_many = providers.Container(
        OneToManyMigrationContainer, clients_repository=clients, multi_facade=multi_facade,
    )
