import pytest

from aiohttp import ClientResponseError
from core.multitable_api.dto import GroupEntity
from core.multitable_api.exceptions import GroupEntityNotFound
from infrastructure.repositories.multitable_api.repository import MultitableUniversityApi


@pytest.fixture()
def group_item() -> GroupEntity:
    return GroupEntity(
        name="ФТ-21001",
        id=1618258658507,
        faculty=1618258396481,
        department=1618258474887,
    )


@pytest.mark.parametrize(
    "responses",
    ([{"name": "ФТ-21001", "id": 1618258658507, "department": 1618258474887, "faculty": 1618258396481}], []),
)
@pytest.mark.asyncio
async def test_get_list_groups(repository: MultitableUniversityApi, responses, mock_request_returned_value):
    mock_request_returned_value(repository, responses)
    result = await repository.groups_get()
    result_dto = [GroupEntity(**row) for row in responses]
    assert result == result_dto


@pytest.mark.asyncio
async def test_get_group(repository: MultitableUniversityApi, group_item, mock_request_returned_value):
    mock_request_returned_value(repository, group_item.dict())
    result = await repository.group_get(identifier=group_item.id)
    assert result == group_item


@pytest.mark.parametrize("status", (404, 500))
@pytest.mark.asyncio
async def test_get_group_error(repository: MultitableUniversityApi, mock_request_returned_value, status):
    mock_request_returned_value(repository, status=status, answer=False)
    with pytest.raises(GroupEntityNotFound):
        await repository.group_get(identifier=1)


@pytest.mark.asyncio
async def test_create_group(repository: MultitableUniversityApi, group_item, mock_request_returned_value):
    mock_request_returned_value(repository, group_item.dict())
    new = await repository.group_create(
        GroupEntity(name=group_item.name, faculty=group_item.faculty, department=group_item.department)
    )
    assert new == group_item


@pytest.mark.asyncio
async def test_create_group_error(repository: MultitableUniversityApi, group_item, mock_request_returned_value):
    mock_request_returned_value(repository, status=500, answer=False)
    with pytest.raises(ClientResponseError):
        await repository.group_create(group_item)


@pytest.mark.asyncio
async def test_update_group(repository: MultitableUniversityApi, group_item, mock_request_returned_value):
    mock_request_returned_value(repository, answer=False)
    group_item.id = "1"
    updated = await repository.group_update(group_item)
    assert updated == group_item
