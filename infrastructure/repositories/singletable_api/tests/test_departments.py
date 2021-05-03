import pytest
from aiohttp import ClientResponseError

from core.singletable_api.dto import DepartmentEntity
from core.singletable_api.exceptions import DepartmentNotFound, DepartmentNotCreated
from core.singletable_api.repository import SingletableUniversityApiBase


@pytest.fixture()
def department_item_with_parent() -> DepartmentEntity:
    return DepartmentEntity(id=1618258396481, parentExtId="parentExtId", name="kdjskdlfsd", extId="1618258396481")


@pytest.fixture()
def department_item_without_parent() -> DepartmentEntity:
    return DepartmentEntity(id=1618511293640, name="kdjskdlfsd", extId="1618258396481")


@pytest.fixture(params=["department_item_with_parent", "department_item_without_parent"])
def department_item(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize(
    "responses",
    (
        [
            {
                "parentExtId": "1618258396481",
                "name": "kdjskdlfsd",
                "extId": "1618258396481",
                "id": 1618258396481,
            },
            {"parentExtId": "1618258396481", "name": "Хлебопекарня", "extId": "1618258568955", "id": 1618511293640},
        ],
        [],
    ),
)
@pytest.mark.asyncio
async def test_get_list_departments(repository: SingletableUniversityApiBase, responses, mock_request_returned_value):
    mock_request_returned_value(repository, responses)
    result = await repository.departments_get()
    result_dto = [DepartmentEntity(**row) for row in responses]
    assert result == result_dto


@pytest.mark.asyncio
async def test_get_department_by_id(
    repository: SingletableUniversityApiBase, department_item, mock_request_returned_value
):
    mock_request_returned_value(repository, department_item.dict())
    result = await repository.department_get_by_id(identifier=department_item.id)
    assert result == department_item


@pytest.mark.asyncio
async def test_get_department_by_ext_id(
    repository: SingletableUniversityApiBase, department_item, mock_request_returned_value
):
    mock_request_returned_value(repository, department_item.dict())
    result = await repository.department_get_by_ext_id(ext_identifier=department_item.extId)
    assert result == department_item


@pytest.mark.parametrize("method", ("department_get_by_id", "department_get_by_ext_id"))
@pytest.mark.parametrize("status", (404, 500))
@pytest.mark.asyncio
async def test_get_department_error(
    repository: SingletableUniversityApiBase, mock_request_returned_value, status, method
):
    mock_request_returned_value(repository, status=status, answer=False)
    with pytest.raises(DepartmentNotFound):
        caller = getattr(repository, method)
        await caller(1)


@pytest.mark.asyncio
async def test_success_create_department(
    repository: SingletableUniversityApiBase, mock_request_returned_value, department_item
):
    mock_request_returned_value(repository, department_item.dict())
    result = await repository.department_create(department=department_item)
    assert result == department_item


@pytest.mark.asyncio
async def test_fail_create_department(
    repository: SingletableUniversityApiBase, mock_request_returned_value, department_item
):
    mock_request_returned_value(repository, status=500)
    with pytest.raises(DepartmentNotCreated):
        await repository.department_create(department=department_item)


@pytest.mark.parametrize("method", ("department_update_by_id", "department_update_by_ext_id"))
@pytest.mark.asyncio
async def test_success_update_department(
    repository: SingletableUniversityApiBase, mock_request_returned_value, department_item, method
):
    mock_request_returned_value(repository, answer=False)
    caller = getattr(repository, method)
    department_item_new = await caller(department=department_item)
    assert department_item_new == department_item


@pytest.mark.parametrize("method", ("department_update_by_id", "department_update_by_ext_id"))
@pytest.mark.parametrize("status", (404, 500))
@pytest.mark.asyncio
async def test_fail_update_department(
    repository: SingletableUniversityApiBase, mock_request_returned_value, status, department_item, method
):
    mock_request_returned_value(repository, status=status, answer=False)
    caller = getattr(repository, method)
    with pytest.raises(ClientResponseError):
        await caller(department=department_item)
