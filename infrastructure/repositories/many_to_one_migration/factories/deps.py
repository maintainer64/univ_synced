from typing import List

from core.multitable_api.entities import DepartmentEntity
from core.singletable_api.entities import DepartmentEntity as SingleDepartmentEntity
from infrastructure.repositories.many_to_one_migration.factories.base import ManyToOneMigrationTemplate


class ManyToOneMigrationDeps(ManyToOneMigrationTemplate):
    async def _get_item(self, identifier: int) -> DepartmentEntity:
        return await self.multi.department_get(identifier=identifier)

    async def _get_data(self) -> List[DepartmentEntity]:
        return await self.multi.departments_get()

    async def caste(self, entity_data: DepartmentEntity) -> SingleDepartmentEntity:
        return SingleDepartmentEntity(
            name=entity_data.name, extId=str(entity_data.id), parentExtId=str(entity_data.faculty)
        )
