from abc import ABC, abstractmethod
from core.many_to_one_migration.dto import MigratedCountingDTO


class ManyToOneMigrationBase(ABC):
    @abstractmethod
    async def migrate(self) -> MigratedCountingDTO:
        ...

    @abstractmethod
    async def migrate_by_id(self, identifier: int) -> bool:
        ...
