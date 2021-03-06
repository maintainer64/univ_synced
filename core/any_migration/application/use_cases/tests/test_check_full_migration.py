from unittest.mock import Mock

import pytest
from asynctest import CoroutineMock

from core.any_migration.application.repository import AnyMigrationBase
from core.any_migration.application.use_cases.full_migration import FullManyToOneMigrationUseCase
from core.any_migration.dto import MigratedCountingDTO


@pytest.fixture()
def counter_mock() -> MigratedCountingDTO:
    return MigratedCountingDTO(success=1, error=1)


@pytest.fixture()
def use_case(counter_mock) -> FullManyToOneMigrationUseCase:
    mock = Mock(spec=AnyMigrationBase)
    mock.migrate = CoroutineMock(return_value=counter_mock)
    return FullManyToOneMigrationUseCase(faculty_migrate=mock, deps_migrate=mock, groups_migrate=mock)


@pytest.mark.asyncio
async def test_success_run(use_case):
    await use_case.execute()
    assert use_case.deps_migrate.migrate.await_count == 3
