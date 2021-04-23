import logging
from core.multi_facade_repository.repository import MultiFacadeRepositoryBase, FunctionDTO
from core.multitable_api.entities import FacultyEntity, DepartmentEntity, GroupEntity
from core.multitable_api.exceptions import EntityNotFound
from core.multitable_api.repository import MultitableUniversityApiBase
from core.singletable_api.entities import DepartmentEntity as SingleDepartmentEntity
from typing import Optional, Union, Dict

from core.tree_single_entity_related.repository import TreeRelatedSingleEntityBase

logger = logging.getLogger(__name__)


class MultiFacadeRepository(MultiFacadeRepositoryBase):
    def __init__(
        self, multi: MultitableUniversityApiBase, single_related: TreeRelatedSingleEntityBase,
    ):
        self.multi = multi
        self.single_related = single_related

    async def caste(
        self, entity: SingleDepartmentEntity
    ) -> Optional[Union[FacultyEntity, DepartmentEntity, GroupEntity]]:
        """
        Переводим объекты одного формата в вид мудльтитабличных
        :param entity:
        :return:
        """
        related_entity = await self.single_related.get_relation(entity=entity)
        if related_entity.level == 1:
            return FacultyEntity(id=int(related_entity.extId), name=related_entity.name)
        elif related_entity.level == 2 and related_entity.parent is not None:
            return DepartmentEntity(
                id=int(related_entity.extId), faculty=int(related_entity.parent.extId), name=related_entity.name
            )
        elif (
            related_entity.level == 3 and related_entity.parent is not None and related_entity.parent.parent is not None
        ):
            return GroupEntity(
                id=int(related_entity.extId),
                faculty=int(related_entity.parent.parent.extId),
                department=int(related_entity.parent.extId),
                name=related_entity.name,
            )
        return None

    async def save(
        self, entity: Union[FacultyEntity, DepartmentEntity, GroupEntity]
    ) -> Union[FacultyEntity, DepartmentEntity, GroupEntity]:
        """
        Сохраняем сущность, не задумываясь, из какой таблицы она есть
        :param entity:
        :return:
        """
        logger.info(f"Сохранение entity в MultiFacadeRepository id={entity.id}")
        client_methods = self._get_function_generic(entity=entity)
        try:
            if entity.id is None:
                raise EntityNotFound()
            await client_methods.get(entity.id)
            # Update
            return await client_methods.update(entity)
        except EntityNotFound:
            # Create
            return await client_methods.create(entity)

    def _get_function_generic(self, entity: Union[FacultyEntity, DepartmentEntity, GroupEntity]) -> FunctionDTO:
        if isinstance(entity, FacultyEntity):
            return FunctionDTO(
                create=self.multi.faculty_create, update=self.multi.faculty_update, get=self.multi.faculty_get
            )
        elif isinstance(entity, DepartmentEntity):
            return FunctionDTO(
                create=self.multi.department_create, update=self.multi.department_update, get=self.multi.department_get
            )
        elif isinstance(entity, GroupEntity):
            return FunctionDTO(create=self.multi.group_create, update=self.multi.group_update, get=self.multi.group_get)

    async def set_cache(self, data: Dict[str, SingleDepartmentEntity]):
        """
        Функция для ускорения работы полной миграции
        :param data:
        :return:
        """
        return await self.single_related.set_cache(data=data)
