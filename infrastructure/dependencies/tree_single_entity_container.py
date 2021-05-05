from dependency_injector import containers, providers

from infrastructure.dependencies.client_service_container import ServiceClientContainer
from infrastructure.repositories.tree_single_entity_related.repository import TreeRelatedSingleEntity


class TreeRelatedSingleEntityContainer(containers.DeclarativeContainer):
    clients_repository: ServiceClientContainer = providers.DependenciesContainer()
    repository = providers.Factory(TreeRelatedSingleEntity, client_single=clients_repository.single)
