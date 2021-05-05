from typing import List

from core.multitable_api.entities import FacultyEntity
from core.singletable_api.entities import DepartmentEntity as SingleDepartmentEntity
from core.singletable_api.exceptions import DepartmentNotFound
from infrastructure.repositories.many_to_one_migration.factories.base import ManyToOneMigrationTemplate


class ManyToOneMigrationFaculties(ManyToOneMigrationTemplate):
    async def _create_root_if_not_exist(self):
        """
        Создать, если не существует корневого элемента
        """
        try:
            # Get
            await self.single.department_get_by_ext_id(ext_identifier="root")
        except DepartmentNotFound:
            # Create
            await self.single.department_create(department=SingleDepartmentEntity(name="Университет", extId="root"))

    async def _get_data(self) -> List[FacultyEntity]:
        await self._create_root_if_not_exist()
        return await self.multi.faculties_get()

    async def _get_item(self, identifier: int) -> FacultyEntity:
        return await self.multi.faculty_get(identifier=identifier)

    async def caste(self, entity_data: FacultyEntity) -> SingleDepartmentEntity:
        return SingleDepartmentEntity(name=entity_data.name, extId=str(entity_data.id), parentExtId="root")
