import pytest
from asynctest import CoroutineMock

from core.multitable_api.dto import FacultyEntity, DepartmentEntity, GroupEntity
from core.singletable_api.dto import DepartmentEntity as SingleDepartmentEntity
from core.singletable_api.exceptions import DepartmentNotFound, DepartmentNotCreated
from infrastructure.repositories.many_to_one_migration.factories.deps import ManyToOneMigrationDeps
from infrastructure.repositories.many_to_one_migration.factories.faculties import ManyToOneMigrationFaculties
from infrastructure.repositories.many_to_one_migration.factories.groups import ManyToOneMigrationGroups


@pytest.fixture()
def repository_faculty(mock_single, mock_multi) -> ManyToOneMigrationFaculties:
    return ManyToOneMigrationFaculties(multi=mock_multi, single=mock_single)


@pytest.fixture()
def data_multi_faculty() -> FacultyEntity:
    return FacultyEntity(id=1, name="Металлургический")


@pytest.fixture()
def data_single_no_id_faculty() -> SingleDepartmentEntity:
    return SingleDepartmentEntity(
        id=None,
        name="Металлургический",
        extId="1",
        parentExtId="root",
    )


@pytest.fixture()
def data_single_faculty(data_single_no_id_faculty) -> SingleDepartmentEntity:
    data = SingleDepartmentEntity.parse_obj(data_single_no_id_faculty)
    data.id = 13794793894
    return data


@pytest.fixture()
def repository_department(mock_single, mock_multi) -> ManyToOneMigrationDeps:
    return ManyToOneMigrationDeps(multi=mock_multi, single=mock_single)


@pytest.fixture()
def data_multi_department() -> DepartmentEntity:
    return DepartmentEntity(id=100, faculty=900, name="ТФКП")


@pytest.fixture()
def data_single_no_id_department() -> SingleDepartmentEntity:
    return SingleDepartmentEntity(
        id=None,
        name="ТФКП",
        extId="100",
        parentExtId="900",
    )


@pytest.fixture()
def data_single_department(data_single_no_id_department) -> SingleDepartmentEntity:
    data = SingleDepartmentEntity.parse_obj(data_single_no_id_department)
    data.id = 13793894384
    return data


@pytest.fixture()
def repository_group(mock_single, mock_multi) -> ManyToOneMigrationGroups:
    return ManyToOneMigrationGroups(multi=mock_multi, single=mock_single)


@pytest.fixture()
def data_multi_group() -> GroupEntity:
    return GroupEntity(id=657, faculty=900, department=100, name="АБС-101010")


@pytest.fixture()
def data_single_no_id_group() -> SingleDepartmentEntity:
    return SingleDepartmentEntity(
        id=None,
        name="АБС-101010",
        extId="657",
        parentExtId="100",
    )


@pytest.fixture()
def data_single_group(data_single_no_id_group) -> SingleDepartmentEntity:
    data = SingleDepartmentEntity.parse_obj(data_single_no_id_group)
    data.id = 137938493057352
    return data


@pytest.fixture(
    params=[
        {"method": "faculties_get", "suffix": "_faculty"},
        {"method": "departments_get", "suffix": "_department"},
        {"method": "groups_get", "suffix": "_group"},
    ]
)
def data_on_success_migration(request):
    suffix = request.param["suffix"]
    return {
        "method": request.param["method"],
        "repository": request.getfixturevalue("repository" + suffix),
        "data_multi": request.getfixturevalue("data_multi" + suffix),
        "data_single": request.getfixturevalue("data_single" + suffix),
        "data_single_no_id": request.getfixturevalue("data_single_no_id" + suffix),
    }


@pytest.mark.asyncio
async def test_success_migration(data_on_success_migration):
    p = data_on_success_migration
    repository = p["repository"]
    setattr(repository.multi, p["method"], CoroutineMock(return_value=[p["data_multi"]]))
    repository.single.department_create = CoroutineMock(return_value=p["data_single"])
    repository.single.department_get_by_ext_id = CoroutineMock(return_value=None)
    await repository.migrate()
    repository.single.department_create.assert_awaited_once_with(department=p["data_single_no_id"])


@pytest.mark.asyncio
async def test_success_migration_and_create_root(
    repository_faculty, data_multi_faculty, data_single_faculty, data_single_no_id_faculty
):
    repository_faculty.multi.faculties_get = CoroutineMock(return_value=[data_multi_faculty])
    repository_faculty.single.department_create = CoroutineMock(return_value=data_single_faculty)
    repository_faculty.single.department_get_by_ext_id = CoroutineMock(side_effect=DepartmentNotFound)
    await repository_faculty.migrate()
    repository_faculty.single.department_create.assert_awaited_with(department=data_single_no_id_faculty)
    assert repository_faculty.single.department_create.await_count == 2


@pytest.mark.asyncio
async def test_success_migration_and_failed_create_root(repository_faculty, data_multi_faculty):
    repository_faculty.multi.faculties_get = CoroutineMock(return_value=[data_multi_faculty])
    repository_faculty.single.department_create = CoroutineMock(side_effect=DepartmentNotCreated)
    repository_faculty.single.department_get_by_ext_id = CoroutineMock(side_effect=DepartmentNotFound)
    await repository_faculty.migrate()
    assert repository_faculty.single.department_create.await_count == 1


@pytest.mark.asyncio
async def test_success_migration_and_update_entity(data_on_success_migration):
    p = data_on_success_migration
    repository = p["repository"]
    setattr(repository.multi, p["method"], CoroutineMock(return_value=[p["data_multi"]]))
    repository.single.department_create = CoroutineMock(side_effect=DepartmentNotCreated)
    repository.single.department_update_by_id = CoroutineMock(return_value=None)
    repository.single.department_get_by_ext_id = CoroutineMock(return_value=p["data_single"])
    await repository.migrate()
    repository.single.department_create.assert_awaited_once_with(department=p["data_single_no_id"])
    repository.single.department_get_by_ext_id.assert_awaited_with(ext_identifier=p["data_single_no_id"].extId)
    repository.single.department_update_by_id.assert_awaited_once_with(department=p["data_single"])
