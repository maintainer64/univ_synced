from dependency_injector import containers, providers

from core.any_migration.application.use_cases.full_migration import FullManyToOneMigrationUseCase
from infrastructure.dependencies.client_service_container import ServiceClientContainer
from infrastructure.repositories.many_to_one_migration.factories.deps import ManyToOneMigrationDeps
from infrastructure.repositories.many_to_one_migration.factories.faculties import ManyToOneMigrationFaculties
from infrastructure.repositories.many_to_one_migration.factories.groups import ManyToOneMigrationGroups


class ManyToOneMigrationContainer(containers.DeclarativeContainer):
    clients_repository: ServiceClientContainer = providers.DependenciesContainer()

    faculty = providers.Factory(
        ManyToOneMigrationFaculties, multi=clients_repository.multi, single=clients_repository.single,
    )
    deps = providers.Factory(ManyToOneMigrationDeps, multi=clients_repository.multi, single=clients_repository.single,)
    groups = providers.Factory(
        ManyToOneMigrationGroups, multi=clients_repository.multi, single=clients_repository.single,
    )


class ManyToOneMigrationUseCasesContainer(containers.DeclarativeContainer):
    migration: ManyToOneMigrationContainer = providers.DependenciesContainer()
    full = providers.Factory(
        FullManyToOneMigrationUseCase,
        faculty_migrate=migration.faculty,
        deps_migrate=migration.deps,
        groups_migrate=migration.groups,
    )
