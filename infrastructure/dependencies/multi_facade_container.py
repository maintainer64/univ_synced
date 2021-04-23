from dependency_injector import containers, providers

from infrastructure.dependencies.client_service_container import ServiceClientContainer
from infrastructure.dependencies.tree_single_entity_container import TreeRelatedSingleEntityContainer
from infrastructure.repositories.multi_facade_repository.repository import MultiFacadeRepository


class MultiFacadeContainer(containers.DeclarativeContainer):
    clients_repository: ServiceClientContainer = providers.DependenciesContainer()
    single_related: TreeRelatedSingleEntityContainer = providers.DependenciesContainer()
    repository = providers.Factory(
        MultiFacadeRepository, multi=clients_repository.multi, single_related=single_related.repository
    )
