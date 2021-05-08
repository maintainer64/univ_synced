from dependency_injector.wiring import inject, Provide

from core.any_migration.application.repository import AnyMigrationBase as Migrate
from core.request_manager.dto import UpdateDataDTO, CreateDataDTO
from infrastructure.repositories.request_manager import router
from infrastructure.dependencies.application_container import ApplicationDependenciesContainer as DD


@router.route(path="/multi/app/faculties", val=CreateDataDTO, methods=["POST"])
@inject
async def faculties_create(
    request: CreateDataDTO, migrate: Migrate = Provide[DD.migration_service_many_to_one.faculty]
):
    await migrate.migrate_by_id(identifier=request.data.id)


@router.route(path="/multi/app/faculties", val=UpdateDataDTO, methods=["PUT"])
@inject
async def faculties_update(
    request: UpdateDataDTO, migrate: Migrate = Provide[DD.migration_service_many_to_one.faculty]
):
    await migrate.migrate_by_id(identifier=request.query.id)


@router.route(path="/multi/app/deps", val=CreateDataDTO, methods=["POST"])
@inject
async def deps_create(request: CreateDataDTO, migrate: Migrate = Provide[DD.migration_service_many_to_one.deps]):
    await migrate.migrate_by_id(identifier=request.data.id)


@router.route(path="/multi/app/deps", val=UpdateDataDTO, methods=["PUT"])
@inject
async def deps_update(request: UpdateDataDTO, migrate: Migrate = Provide[DD.migration_service_many_to_one.deps]):
    await migrate.migrate_by_id(identifier=request.query.id)


@router.route(path="/multi/app/groups", val=CreateDataDTO, methods=["POST"])
@inject
async def groups_create(request: CreateDataDTO, migrate: Migrate = Provide[DD.migration_service_many_to_one.groups]):
    await migrate.migrate_by_id(identifier=request.data.id)


@router.route(path="/multi/app/groups", val=UpdateDataDTO, methods=["PUT"])
@inject
async def groups_update(request: UpdateDataDTO, migrate: Migrate = Provide[DD.migration_service_many_to_one.groups]):
    await migrate.migrate_by_id(identifier=request.query.id)
