import pytest
from asynctest import CoroutineMock

from core.multitable_api.entities import DepartmentEntity
from core.singletable_api.entities import DepartmentEntity as SingleDepartmentEntity
from infrastructure.repositories.one_to_many_migration.repository import OneToManyMigration


@pytest.fixture()
def repository(mock_single, mock_multi_facade):
    return OneToManyMigration(multi_facade=mock_multi_facade, single=mock_single,)


@pytest.fixture()
def single_departments_entity():
    return SingleDepartmentEntity(id=2, name="Департамент", extId="800", parentExtId="900")


@pytest.fixture()
def caste_entity():
    return DepartmentEntity(id=800, name="Департамент", faculty=900)


@pytest.mark.asyncio
async def test_migrate_full_data(repository, single_departments_entity, caste_entity):
    repository.single.departments_get = CoroutineMock(return_value=[single_departments_entity])
    repository.multi_facade.set_cache = CoroutineMock()
    repository.multi_facade.caste = CoroutineMock(return_value=caste_entity)
    repository.multi_facade.save = CoroutineMock(return_value=caste_entity)
    counter = await repository.migrate()
    assert counter.success == 1
    repository.multi_facade.set_cache.assert_awaited_once_with(
        data={single_departments_entity.extId: single_departments_entity}
    )
    repository.multi_facade.caste.assert_awaited_once_with(entity=single_departments_entity)
    repository.multi_facade.save.assert_awaited_once_with(entity=caste_entity)


@pytest.mark.asyncio
async def test_migrate_full_data_caste_error(repository, single_departments_entity, caste_entity):
    repository.single.departments_get = CoroutineMock(return_value=[single_departments_entity])
    repository.multi_facade.set_cache = CoroutineMock()
    repository.multi_facade.caste = CoroutineMock(return_value=None)
    repository.multi_facade.save = CoroutineMock(return_value=caste_entity)
    counter = await repository.migrate()
    assert counter.success == 0
    assert counter.error == 1
    repository.multi_facade.set_cache.assert_awaited_once_with(
        data={single_departments_entity.extId: single_departments_entity}
    )
    repository.multi_facade.caste.assert_awaited_once_with(entity=single_departments_entity)
    repository.multi_facade.save.assert_not_awaited()


@pytest.mark.asyncio
async def test_migrate_get_data_error(repository):
    repository.single.departments_get = CoroutineMock(side_effect=Exception)
    repository.multi_facade.set_cache = CoroutineMock()
    repository.multi_facade.caste = CoroutineMock()
    repository.multi_facade.save = CoroutineMock()
    counter = await repository.migrate()
    assert counter.success == 0
    assert counter.error == 0
    repository.multi_facade.set_cache.assert_not_awaited()
    repository.multi_facade.caste.assert_not_awaited()
    repository.multi_facade.save.assert_not_awaited()


@pytest.mark.asyncio
async def test_migrate_save_data_error(repository, single_departments_entity, caste_entity):
    repository.single.departments_get = CoroutineMock(return_value=[single_departments_entity])
    repository.multi_facade.set_cache = CoroutineMock()
    repository.multi_facade.caste = CoroutineMock(return_value=caste_entity)
    repository.multi_facade.save = CoroutineMock(side_effect=Exception)
    counter = await repository.migrate()
    assert counter.success == 0
    assert counter.error == 1
    repository.multi_facade.set_cache.assert_awaited_once_with(
        data={single_departments_entity.extId: single_departments_entity}
    )
    repository.multi_facade.caste.assert_awaited_once_with(entity=single_departments_entity)
    repository.multi_facade.save.assert_awaited_once_with(entity=caste_entity)


@pytest.mark.parametrize(
    "function", (("department_get_by_id", "migrate_by_id"), ("department_get_by_ext_id", "migrate_by_ext_id"))
)
@pytest.mark.asyncio
async def test_migrate_by_id_data(repository, function, single_departments_entity, caste_entity):
    client_f = CoroutineMock(return_value=single_departments_entity)
    setattr(repository.single, function[0], client_f)
    repo_f = getattr(repository, function[1])
    repository.multi_facade.caste = CoroutineMock(return_value=caste_entity)
    repository.multi_facade.save = CoroutineMock(return_value=caste_entity)
    is_ok = await repo_f(1)
    assert is_ok is True
    repository.multi_facade.caste.assert_awaited_once_with(entity=single_departments_entity)
    repository.multi_facade.save.assert_awaited_once_with(entity=caste_entity)
