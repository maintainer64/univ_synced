import pytest
from pydantic import BaseModel, ValidationError
from infrastructure.repositories.client_template.validators import validate_dict, validate_list


@pytest.fixture()
def pydantic_class():
    class Class(BaseModel):
        field_a: int
        field_b: str

    return Class


@pytest.fixture()
def pydantic_class_data():
    return {"field_a": 38, "field_b": "jjj"}


@pytest.mark.parametrize("data", ((18, TypeError), ({"field_c": 38}, ValidationError)))
def test_validator_dict_error(data, pydantic_class):
    resp, raise_ = data
    with pytest.raises(raise_):
        validate_dict(resp, pydantic_class)


def test_validator_dict_success(pydantic_class, pydantic_class_data):
    obj = validate_dict(pydantic_class_data, pydantic_class)
    assert obj == pydantic_class(**pydantic_class_data)


def test_validator_list_success(pydantic_class, pydantic_class_data):
    obj = validate_list([pydantic_class_data], pydantic_class)
    assert obj == [pydantic_class(**pydantic_class_data)]
