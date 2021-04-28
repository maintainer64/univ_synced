import pytest

from aiohttp import ClientResponseError
from core.multitable_api.dto import DepartmentEntity
from core.multitable_api.exceptions import DepartmentEntityNotFound
from infrastructure.repositories.multitable_api.repository import MultitableUniversityApi


@pytest.fixture()
def department_item() -> DepartmentEntity:
    return DepartmentEntity(name="Вычислительной техники", id=1618258474887, faculty=1618258396481)


@pytest.mark.parametrize(
    "responses",
    (
        [
            {"name": "Вычислительной техники", "id": 1618258474887, "faculty": 1618258396481},
            {"name": "Архитектуры", "id": 1618258568955, "faculty": 1618258419920},
            {"name": "Гидравлики", "id": 1618258575976, "faculty": 1618258419920},
        ],
        [],
    ),
)
@pytest.mark.asyncio
async def test_get_list_departments(repository: MultitableUniversityApi, responses, mock_request_returned_value):
    mock_request_returned_value(repository, responses)
    result = await repository.departments_get()
    result_dto = [DepartmentEntity(**row) for row in responses]
    assert result == result_dto


@pytest.mark.asyncio
async def test_get_department(repository: MultitableUniversityApi, department_item, mock_request_returned_value):
    mock_request_returned_value(repository, department_item.dict())
    result = await repository.department_get(identifier=department_item.id)
    assert result == department_item


@pytest.mark.parametrize("status", (404, 500))
@pytest.mark.asyncio
async def test_get_department_error(repository: MultitableUniversityApi, mock_request_returned_value, status):
    mock_request_returned_value(repository, status=status, answer=False)
    with pytest.raises(DepartmentEntityNotFound):
        await repository.department_get(identifier=1)


@pytest.mark.asyncio
async def test_create_department(repository: MultitableUniversityApi, department_item, mock_request_returned_value):
    mock_request_returned_value(repository, department_item.dict())
    new = await repository.department_create(
        DepartmentEntity(name=department_item.name, faculty=department_item.faculty)
    )
    assert new == department_item


@pytest.mark.asyncio
async def test_create_faculty_error(repository: MultitableUniversityApi, department_item, mock_request_returned_value):
    mock_request_returned_value(repository, status=500, answer=False)
    with pytest.raises(ClientResponseError):
        await repository.department_create(department_item)


@pytest.mark.asyncio
async def test_update_faculty(repository: MultitableUniversityApi, department_item, mock_request_returned_value):
    mock_request_returned_value(repository, answer=False)
    department_item.id = "1"
    updated = await repository.department_update(department_item)
    assert updated == department_item
