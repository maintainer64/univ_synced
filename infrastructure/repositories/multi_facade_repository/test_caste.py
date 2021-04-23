from unittest.mock import Mock

import pytest
from asynctest import CoroutineMock

from core.multitable_api.exceptions import FacultyEntityNotFound, DepartmentEntityNotFound, GroupEntityNotFound
from core.multitable_api.entities import FacultyEntity, DepartmentEntity, GroupEntity
from core.tree_single_entity_related.dto import SingleRelationDepartmentDTO
from infrastructure.repositories.multi_facade_repository.repository import MultiFacadeRepository


@pytest.fixture()
def repository(mock_multi, mock_tree_single) -> MultiFacadeRepository:
    return MultiFacadeRepository(multi=mock_multi, single_related=mock_tree_single)


@pytest.fixture()
def root():
    return SingleRelationDepartmentDTO(id=0, name="Университет", extId="root")


@pytest.fixture()
def level_1(root):
    z = SingleRelationDepartmentDTO(id=1, name="Факультет", extId="900", parentExtId="root")
    return z.set_parent(root)


@pytest.fixture()
def level_2(level_1):
    z = SingleRelationDepartmentDTO(id=2, name="Департамент", extId="800", parentExtId="900")
    return z.set_parent(level_1)


@pytest.fixture()
def level_3(level_2):
    z = SingleRelationDepartmentDTO(id=3, name="Группа", extId="700", parentExtId="800")
    return z.set_parent(level_2)


@pytest.fixture()
def level_1_multi():
    return FacultyEntity(id=900, name="Факультет")


@pytest.fixture()
def level_2_multi():
    return DepartmentEntity(id=800, faculty=900, name="Департамент")


@pytest.fixture()
def level_3_multi():
    return GroupEntity(id=700, faculty=900, department=800, name="Группа")


@pytest.fixture(params=[str(i) for i in range(1, 4)])
def checker_level(request):
    return (request.getfixturevalue(f"level_{request.param}"), request.getfixturevalue(f"level_{request.param}_multi"))


@pytest.mark.asyncio
async def test_caste(repository, checker_level):
    req, resp = checker_level
    repository.single_related.get_relation = CoroutineMock(return_value=req)
    resp_caste = await repository.caste(None)
    assert resp_caste == resp


@pytest.mark.asyncio
async def test_caste_root(repository):
    mock = Mock(spec=SingleRelationDepartmentDTO)
    mock.level = Mock(return_value=0)
    repository.single_related.get_relation = CoroutineMock(return_value=mock)
    resp_caste = await repository.caste(None)
    assert resp_caste is None


@pytest.fixture()
def saved_functions(
    level_1_multi, level_2_multi, level_3_multi,
):
    return (
        ("faculty_create", "faculty_update", "faculty_get", level_1_multi, FacultyEntityNotFound),
        ("department_create", "department_update", "department_get", level_2_multi, DepartmentEntityNotFound),
        ("group_create", "group_update", "group_get", level_3_multi, GroupEntityNotFound),
    )


@pytest.mark.asyncio
async def test_save_entity(repository: MultiFacadeRepository, saved_functions):
    for create, _, get, entity, exception in saved_functions:
        c = CoroutineMock(return_value=entity)
        g = CoroutineMock(side_effect=exception)
        setattr(repository.multi, create, c)
        setattr(repository.multi, get, g)
        await repository.save(entity)
        c.assert_awaited_once_with(entity)
        g.assert_awaited_once_with(entity.id)


@pytest.mark.asyncio
async def test_save_entity_no_id(repository: MultiFacadeRepository, saved_functions):
    for create, _, get, entity, exception in saved_functions:
        entity.id = None
        c = CoroutineMock(return_value=entity)
        setattr(repository.multi, create, c)
        await repository.save(entity)
        c.assert_awaited_once_with(entity)


@pytest.mark.asyncio
async def test_update_entity(repository: MultiFacadeRepository, saved_functions):
    for create, update, get, entity, _ in saved_functions:
        c = CoroutineMock()
        u = CoroutineMock(return_value=entity)
        g = CoroutineMock(return_value=entity)
        setattr(repository.multi, create, c)
        setattr(repository.multi, get, g)
        setattr(repository.multi, update, u)
        await repository.save(entity)
        c.assert_not_awaited()
        u.assert_awaited_once_with(entity)
        g.assert_awaited_once_with(entity.id)


@pytest.mark.asyncio
async def test_update_entity_error(repository: MultiFacadeRepository, saved_functions):
    for _, update, get, entity, _ in saved_functions:
        g = CoroutineMock(return_value=entity)
        u = CoroutineMock(side_effect=Exception)
        setattr(repository.multi, get, g)
        setattr(repository.multi, update, u)
        with pytest.raises(Exception):
            await repository.save(entity)
        g.assert_awaited_once_with(entity.id)
        u.assert_awaited_once_with(entity)


@pytest.mark.asyncio
async def test_no_save_entity(repository):
    with pytest.raises(AttributeError):
        await repository.save(1892)


@pytest.mark.asyncio
async def test_set_cache_call(repository):
    repository.single_related.set_cache = CoroutineMock()
    await repository.set_cache(dict())
    repository.single_related.set_cache.assert_awaited_once_with(data=dict())
