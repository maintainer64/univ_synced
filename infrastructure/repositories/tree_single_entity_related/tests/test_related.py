import pytest
from asynctest import CoroutineMock, call

from core.singletable_api.exceptions import DepartmentNotFound
from core.singletable_api.entities import DepartmentEntity as SingleDepartmentEntity
from infrastructure.repositories.tree_single_entity_related.repository import TreeRelatedSingleEntity


@pytest.fixture()
def repository(mock_single):
    return TreeRelatedSingleEntity(client_single=mock_single)


@pytest.fixture()
def entity_no_relationship():
    return SingleDepartmentEntity(id=3, name="Группа", extId="700", parentExtId="800")


@pytest.fixture()
def related_entity_list():
    return [
        SingleDepartmentEntity(id=2, name="Департамент", extId="800", parentExtId="900"),
        SingleDepartmentEntity(id=1, name="Факультет", extId="900", parentExtId="root"),
        SingleDepartmentEntity(id=0, name="Университет", extId="root",),
    ]


@pytest.fixture()
def related_warning_list(related_entity_list):
    related_entity_list[-1].parentExtId = "warning"
    related_entity_list.append(DepartmentNotFound)
    return related_entity_list


async def checker_related(repository, entity_no_relationship):
    relationship = await repository.get_relation(entity=entity_no_relationship)
    assert relationship.level == 3
    assert relationship.parent.level == 2
    assert relationship.parent.parent.level == 1
    assert relationship.parent.parent.parent.level == 0


@pytest.mark.asyncio
async def test_success_related(repository, entity_no_relationship, related_entity_list):
    repository.client.department_get_by_ext_id = CoroutineMock(side_effect=related_entity_list)
    await checker_related(
        repository=repository, entity_no_relationship=entity_no_relationship,
    )
    repository.client.department_get_by_ext_id.assert_has_awaits(
        calls=(call(ext_identifier="800"), call(ext_identifier="900"), call(ext_identifier="root"),), any_order=False
    )


@pytest.mark.asyncio
async def test_success_cache_related(repository, entity_no_relationship, related_entity_list):
    repository.client.department_get_by_ext_id = CoroutineMock(return_value=False)
    await repository.set_cache(dict((x.extId, x) for x in related_entity_list))
    assert repository._cache is not None
    await checker_related(
        repository=repository, entity_no_relationship=entity_no_relationship,
    )
    repository.client.department_get_by_ext_id.assert_not_awaited()


@pytest.mark.asyncio
async def test_warning_related(repository, entity_no_relationship, related_warning_list):
    repository.client.department_get_by_ext_id = CoroutineMock(side_effect=related_warning_list)
    await checker_related(
        repository=repository, entity_no_relationship=entity_no_relationship,
    )
    repository.client.department_get_by_ext_id.assert_has_awaits(
        calls=(
            call(ext_identifier="800"),
            call(ext_identifier="900"),
            call(ext_identifier="root"),
            call(ext_identifier="warning"),
        ),
        any_order=False,
    )


@pytest.mark.asyncio
async def test_related_cache_and_not_cache(repository, entity_no_relationship, related_warning_list):
    await repository.set_cache(dict((x.extId, x) for x in related_warning_list[:1]))
    assert repository._cache is not None
    repository.client.department_get_by_ext_id = CoroutineMock(side_effect=related_warning_list[1:])
    await checker_related(
        repository=repository, entity_no_relationship=entity_no_relationship,
    )
    repository.client.department_get_by_ext_id.assert_has_awaits(
        calls=(call(ext_identifier="900"), call(ext_identifier="root"), call(ext_identifier="warning"),),
        any_order=False,
    )
