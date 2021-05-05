import pytest
from unittest.mock import Mock

from aiohttp import ClientResponse, ClientResponseError, RequestInfo
from asynctest import CoroutineMock

from core.multi_facade_repository.repository import MultiFacadeRepositoryBase
from core.multitable_api.repository import MultitableUniversityApiBase
from core.singletable_api.repository import SingletableUniversityApiBase
from core.tree_single_entity_related.repository import TreeRelatedSingleEntityBase


@pytest.fixture()
def mock_single() -> SingletableUniversityApiBase:
    return Mock(spec=SingletableUniversityApiBase)


@pytest.fixture()
def mock_multi() -> MultitableUniversityApiBase:
    return Mock(spec=MultitableUniversityApiBase)


@pytest.fixture()
def mock_tree_single() -> TreeRelatedSingleEntityBase:
    return Mock(spec=TreeRelatedSingleEntityBase)


@pytest.fixture()
def mock_multi_facade() -> MultiFacadeRepositoryBase:
    return Mock(spec=MultiFacadeRepositoryBase)


@pytest.fixture()
def mock_request_returned_value():
    def wrap(api_repo, json_data_resp=None, status=200, answer=True):
        resp = Mock(spec=ClientResponse)
        resp.status = status
        if 400 <= status:
            api_repo.session.request = CoroutineMock(
                side_effect=ClientResponseError(
                    status=status, request_info=RequestInfo(url="/", method="", headers=dict()), history=(),
                )
            )
        else:
            if answer:
                resp.json = CoroutineMock(return_value=json_data_resp)
            api_repo.session.request = CoroutineMock(return_value=resp)

    return wrap
