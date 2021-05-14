from dependency_injector.wiring import inject, Provide

from core.any_migration.application.repository import AnyMigrationBase as Migrate
from core.one_to_many_migration.repository import SingleMigrationBase
from core.request_manager.dto import UpdateDataDTO, CreateDataDTO, DepartmentUpdateExtDataDTO
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


@router.route(path="/single/app/departments", val=CreateDataDTO, methods=["POST"])
@inject
async def departments_create(
    request: CreateDataDTO, migrate: SingleMigrationBase = Provide[DD.migration_service_one_to_many.repository]
):
    await migrate.migrate_by_id(identifier=request.data.id)


@router.route(path="/single/app/departments", val=DepartmentUpdateExtDataDTO, methods=["PUT"])
@inject
async def departments_update(
    request: DepartmentUpdateExtDataDTO,
    migrate: SingleMigrationBase = Provide[DD.migration_service_one_to_many.repository],
):
    if request.query.id is not None:
        await migrate.migrate_by_id(identifier=request.query.id)
    elif request.query.ext is not None:
        await migrate.migrate_by_ext_id(identifier=request.query.ext)
