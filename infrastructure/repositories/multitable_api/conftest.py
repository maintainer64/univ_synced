import pytest
from unittest.mock import Mock

from aiohttp import ClientSession
from infrastructure.repositories.multitable_api.repository import MultitableUniversityApi


@pytest.fixture()
async def repository() -> MultitableUniversityApi:
    session = Mock(spec=ClientSession)
    return MultitableUniversityApi(base_url="http://", session=session)
