import pytest

from aiohttp import ClientResponseError
from core.multitable_api.dto import FacultyEntity
from core.multitable_api.exceptions import FacultyEntityNotFound
from infrastructure.repositories.multitable_api.repository import MultitableUniversityApi


@pytest.fixture()
def faculty_item() -> FacultyEntity:
    return FacultyEntity(name="Физико-технический", id=1618258396481)


@pytest.mark.parametrize(
    "responses",
    ([{"name": "Физико-технический", "id": 1618258396481}, {"name": "Строительный", "id": 1618258419920}], []),
)
@pytest.mark.asyncio
async def test_get_list_faculties(repository: MultitableUniversityApi, responses, mock_request_returned_value):
    mock_request_returned_value(repository, responses)
    result = await repository.faculties_get()
    result_dto = [FacultyEntity(**row) for row in responses]
    assert result == result_dto


@pytest.mark.asyncio
async def test_get_faculty(repository: MultitableUniversityApi, faculty_item, mock_request_returned_value):
    mock_request_returned_value(repository, faculty_item.dict())
    result = await repository.faculty_get(identifier=faculty_item.id)
    assert result == faculty_item


@pytest.mark.parametrize("status", (404, 500))
@pytest.mark.asyncio
async def test_get_faculty_error(repository: MultitableUniversityApi, mock_request_returned_value, status):
    mock_request_returned_value(repository, status=status, answer=False)
    with pytest.raises(FacultyEntityNotFound):
        await repository.faculty_get(identifier=1)


@pytest.mark.asyncio
async def test_create_faculty(repository: MultitableUniversityApi, faculty_item, mock_request_returned_value):
    mock_request_returned_value(repository, faculty_item.dict())
    faculty_item_new = await repository.faculty_create(FacultyEntity(name=faculty_item.name))
    assert faculty_item_new == faculty_item


@pytest.mark.asyncio
async def test_create_faculty_error(repository: MultitableUniversityApi, faculty_item, mock_request_returned_value):
    mock_request_returned_value(repository, status=500, answer=False)
    with pytest.raises(ClientResponseError):
        await repository.faculty_create(FacultyEntity(name=faculty_item.name))


@pytest.mark.asyncio
async def test_update_faculty(repository: MultitableUniversityApi, faculty_item, mock_request_returned_value):
    mock_request_returned_value(repository, answer=False)
    faculty_item.id = "1"
    faculty_item_updated = await repository.faculty_update(faculty_item)
    assert faculty_item_updated == faculty_item
