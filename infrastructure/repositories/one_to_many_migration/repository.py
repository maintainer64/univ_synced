import logging
from typing import Dict


from core.any_migration.dto import MigratedCountingDTO
from core.any_migration.application.repository import AnyMigrationBase
from core.multi_facade_repository.repository import MultiFacadeRepositoryBase
from core.singletable_api.repository import SingletableUniversityApiBase
from core.singletable_api.entities import DepartmentEntity as SingleDepartmentEntity

logger = logging.getLogger(__name__)


class OneToManyMigration(AnyMigrationBase):
    def __init__(self, single: SingletableUniversityApiBase, multi_facade: MultiFacadeRepositoryBase):
        self.multi_facade = multi_facade
        self.single = single

    async def migrate(self) -> MigratedCountingDTO:
        logger.info("Началась миграция из Single в Multi")
        counter = MigratedCountingDTO(success=0, error=0)
        try:
            entity_dict = await self._get_data()
            await self.multi_facade.set_cache(data=entity_dict)
        except Exception as err:
            logging.exception("Not related data in OneToManyMigration", extra={"error": err})
            return counter

        for entity in entity_dict.values():
            if await self._migrate_item(entity=entity):
                counter.success += 1
            else:
                counter.error += 1
        return counter

    async def migrate_by_id(self, identifier: int) -> bool:
        logger.info(f"Началась миграция из Single в Multi по id={identifier}")
        single_department = await self.single.department_get_by_id(identifier=identifier)
        return await self._migrate_item(entity=single_department)

    async def migrate_by_ext_id(self, identifier: str) -> bool:
        logger.info(f"Началась миграция из Single в Multi по ext_id={identifier}")
        single_department = await self.single.department_get_by_ext_id(ext_identifier=identifier)
        return await self._migrate_item(entity=single_department)

    async def _get_data(self) -> Dict[str, SingleDepartmentEntity]:
        data = await self.single.departments_get()
        return dict((x.extId, x) for x in data)

    async def _migrate_item(self, entity: SingleDepartmentEntity) -> bool:
        try:
            entity_caste = await self.multi_facade.caste(entity=entity)
            if entity_caste is None:
                logging.info(f"SingleDepartmentEntity is not caste id={entity.id}")
                return False
            await self.multi_facade.save(entity=entity_caste)
            return True
        except Exception as err:
            logging.exception("Not save or caste data in OneToManyMigration", extra={"error": err, "id": entity.id})
        return False
