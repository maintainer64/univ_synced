import pytest
from asynctest import CoroutineMock
from starlette.testclient import TestClient

from infrastructure.repositories.request_manager import RequestApplicationManager


@pytest.fixture()
def function_one_param():
    async def function(param: str):
        return param + "900"

    return function


@pytest.mark.parametrize("argument", ("first", "second"))
@pytest.mark.asyncio
async def test_not_changed_original_function(function_one_param, argument):
    router = RequestApplicationManager()
    function_one_param_new = router.route("/", "id")(function_one_param)
    assert await function_one_param(argument) == await function_one_param_new(argument)
    assert function_one_param.__name__ == function_one_param_new.__name__


@pytest.fixture()
def client_and_func():
    function_mock = CoroutineMock(return_value="100")
    router = RequestApplicationManager()
    router.route("/", "id")(function_mock)
    return TestClient(router.get_server()), function_mock


@pytest.mark.parametrize("method", ("POST", "PUT"))
@pytest.mark.parametrize("argument", ("first", "second"))
def test_working_function(client_and_func, argument, method):
    client: TestClient = client_and_func[0]
    func: CoroutineMock = client_and_func[1]
    data = client.request(method=method, url="/", params={"id": argument})
    assert data.status_code == 200
    func.assert_awaited_once_with(argument)


@pytest.mark.parametrize("method", ("POST", "PUT"))
@pytest.mark.parametrize("params", (None, {"id": None}, {"guid": "valid"}))
def test_error_wrapper(client_and_func, params, method):
    client: TestClient = client_and_func[0]
    func: CoroutineMock = client_and_func[1]
    data = client.request(method=method, url="/", params=params)
    assert data.status_code == 500
    func.assert_not_awaited()


@pytest.mark.parametrize("params", (None, {"id": None}, {"guid": "valid"}, {"id": "valid"}))
def test_error_wrapper_get_method(client_and_func, params):
    client: TestClient = client_and_func[0]
    func: CoroutineMock = client_and_func[1]
    data = client.request(method="GET", url="/", params=params)
    assert data.status_code != 200
    func.assert_not_awaited()
