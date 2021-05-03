import pytest
from unittest.mock import Mock

from aiohttp import ClientSession
from infrastructure.repositories.singletable_api.repository import SingletableUniversityApi


@pytest.fixture()
async def repository() -> SingletableUniversityApi:
    session = Mock(spec=ClientSession)
    return SingletableUniversityApi(base_url="http://", session=session)
