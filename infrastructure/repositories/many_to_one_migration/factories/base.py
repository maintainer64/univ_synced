import logging
from abc import ABC, abstractmethod
from typing import List, Any

from core.many_to_one_migration.dto import MigratedCountingDTO
from core.many_to_one_migration.application.repository import ManyToOneMigrationBase
from core.multitable_api.repository import MultitableUniversityApiBase
from core.singletable_api.exceptions import DepartmentNotCreated
from core.singletable_api.repository import SingletableUniversityApiBase
from core.singletable_api.dto import DepartmentEntity as SingleDepartmentEntity


class ManyToOneMigrationTemplate(ManyToOneMigrationBase, ABC):
    def __init__(self, multi: MultitableUniversityApiBase, single: SingletableUniversityApiBase):
        self.multi = multi
        self.single = single

    async def migrate(self) -> MigratedCountingDTO:
        counter = MigratedCountingDTO(success=0, error=0)
        try:
            entity_list = await self._get_data()
        except Exception as err:
            logging.exception("Not related data in ManyToOneMigration", extra={"error": err})
            return counter

        for entity in entity_list:
            try:
                entity_caste = await self._caste(entity_data=entity,)
                await self._save(entity_data=entity_caste)
                counter.success += 1
            except Exception as err:
                counter.error += 1
                logging.exception("Not save or caste data in ManyToOneMigration", extra={"error": err})
        return counter

    async def migrate_by_id(self, identifier: int) -> bool:
        try:
            entity = await self._get_item(identifier=identifier)
            entity_caste = await self._caste(entity_data=entity,)
            await self._save(entity_data=entity_caste)
            return True
        except Exception as err:
            logging.exception("Error migrate item in ManyToOneMigration", extra={"error": err})
        return False

    @abstractmethod
    async def _get_data(self) -> List[Any]:
        ...

    @abstractmethod
    async def _get_item(self, identifier: int) -> Any:
        ...

    @abstractmethod
    async def _caste(self, entity_data: Any) -> SingleDepartmentEntity:
        ...

    async def _save(self, entity_data: SingleDepartmentEntity):
        try:
            await self.single.department_create(department=entity_data)
        except DepartmentNotCreated:
            entity_data_single = await self.single.department_get_by_ext_id(ext_identifier=entity_data.extId)
            entity_data_single.update(entity_data)
            await self.single.department_update_by_id(department=entity_data_single)
