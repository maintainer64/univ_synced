import pytest
from unittest.mock import Mock

from aiohttp import ClientResponse, ClientResponseError, RequestInfo
from asynctest import CoroutineMock


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
