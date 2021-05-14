from core.any_migration.application.repository import AnyMigrationBase
from abc import ABC, abstractmethod


class SingleMigrationBase(AnyMigrationBase, ABC):
    @abstractmethod
    async def migrate_by_ext_id(self, identifier: str) -> bool:
        ...
