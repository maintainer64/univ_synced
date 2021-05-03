from unittest.mock import Mock

import pytest

from core.multitable_api.repository import MultitableUniversityApiBase
from core.singletable_api.repository import SingletableUniversityApiBase


@pytest.fixture()
def mock_single() -> SingletableUniversityApiBase:
    return Mock(spec=SingletableUniversityApiBase)


@pytest.fixture()
def mock_multi() -> MultitableUniversityApiBase:
    return Mock(spec=MultitableUniversityApiBase)
