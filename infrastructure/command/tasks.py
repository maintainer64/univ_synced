from dependency_injector.wiring import inject, Provide

from core.many_to_one_migration.application.use_cases.full_migration import FullManyToOneMigrationUseCase
from infrastructure.dependencies.application_container import ApplicationDependenciesContainer as DD


@inject
async def run(
    use_case: FullManyToOneMigrationUseCase = Provide[DD.migration_service_many_to_one_use_cases.full],
):
    await use_case.execute()
