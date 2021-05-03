from typing import List

from core.multitable_api.dto import GroupEntity
from core.singletable_api.dto import DepartmentEntity as SingleDepartmentEntity
from infrastructure.repositories.many_to_one_migration.factories.base import ManyToOneMigrationTemplate


class ManyToOneMigrationGroups(ManyToOneMigrationTemplate):
    async def _get_item(self, identifier: int) -> GroupEntity:
        return await self.multi.group_get(identifier=identifier)

    async def _get_data(self) -> List[GroupEntity]:
        return await self.multi.groups_get()

    async def _caste(self, entity_data: GroupEntity) -> SingleDepartmentEntity:
        return SingleDepartmentEntity(
            name=entity_data.name, extId=str(entity_data.id), parentExtId=str(entity_data.department)
        )
