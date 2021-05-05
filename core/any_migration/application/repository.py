from abc import ABC, abstractmethod
from core.any_migration.dto import MigratedCountingDTO
from typing import TypeVar, Generic

TCastleObject = TypeVar("TCastleObject")
TOutCastleObject = TypeVar("TOutCastleObject")
TSaverObject = TypeVar("TSaverObject")


class AnyMigrationBase(ABC):
    @abstractmethod
    async def migrate(self) -> MigratedCountingDTO:
        ...

    @abstractmethod
    async def migrate_by_id(self, identifier: int) -> bool:
        ...


class AnyCaster(Generic[TCastleObject, TOutCastleObject]):
    @abstractmethod
    async def caste(self, entity: TCastleObject) -> TOutCastleObject:
        ...


class AnySaver(Generic[TSaverObject]):
    @abstractmethod
    async def save(self, entity: TSaverObject) -> TSaverObject:
        ...
