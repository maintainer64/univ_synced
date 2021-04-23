from dependency_injector import containers, providers

from infrastructure.dependencies.client_service_container import ServiceClientContainer
from infrastructure.dependencies.multi_facade_container import MultiFacadeContainer
from infrastructure.repositories.one_to_many_migration.repository import OneToManyMigration


class OneToManyMigrationContainer(containers.DeclarativeContainer):
    clients_repository: ServiceClientContainer = providers.DependenciesContainer()
    multi_facade: MultiFacadeContainer = providers.DependenciesContainer()
    repository = providers.Factory(
        OneToManyMigration, multi_facade=multi_facade.repository, single=clients_repository.single
    )
