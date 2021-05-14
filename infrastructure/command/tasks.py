from dependency_injector.wiring import inject, Provide

from core.any_migration.application.use_cases.full_migration import FullManyToOneMigrationUseCase
from core.one_to_many_migration.repository import SingleMigrationBase
from infrastructure.dependencies.application_container import ApplicationDependenciesContainer as DD


@inject
async def many_to_one_full_migrate(
    use_case: FullManyToOneMigrationUseCase = Provide[DD.migration_service_many_to_one_use_cases.full],
):
    await use_case.execute()


@inject
async def one_to_many_full_migrate(
    repository: SingleMigrationBase = Provide[DD.migration_service_one_to_many.repository],
):
    await repository.migrate()


async def full_migrate():
    await many_to_one_full_migrate()
    await one_to_many_full_migrate()
