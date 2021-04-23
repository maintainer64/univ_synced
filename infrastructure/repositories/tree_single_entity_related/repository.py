import logging
from typing import Dict, Optional
from core.singletable_api.entities import DepartmentEntity as SingleDepartmentEntity
from core.singletable_api.exceptions import DepartmentNotFound
from core.singletable_api.repository import SingletableUniversityApiBase
from core.tree_single_entity_related.dto import SingleRelationDepartmentDTO
from core.tree_single_entity_related.repository import TreeRelatedSingleEntityBase

logger = logging.getLogger(__name__)


class TreeRelatedSingleEntity(TreeRelatedSingleEntityBase):
    def __init__(self, client_single: SingletableUniversityApiBase):
        self.client = client_single
        self._cache: Dict[str, SingleDepartmentEntity] = dict()

    async def set_cache(self, data: Dict[str, SingleDepartmentEntity]):
        self._cache.update(data)

    async def _get_data_by_ext_id(self, ext_id: Optional[str]) -> Optional[SingleDepartmentEntity]:
        """
        Save cache in object
        :param ext_id:
        :return:
        """
        if ext_id is None:
            return None
        if ext_id in self._cache:
            return self._cache[ext_id]
        try:
            entity = await self.client.department_get_by_ext_id(ext_identifier=ext_id)
        except DepartmentNotFound:
            return None
        self._cache[ext_id] = entity
        return entity

    async def _loaded_parent_data(self, entity: SingleDepartmentEntity) -> SingleRelationDepartmentDTO:
        related_entity = SingleRelationDepartmentDTO.parse_obj(entity)
        original_parent_entity = await self._get_data_by_ext_id(ext_id=entity.parentExtId)
        if original_parent_entity is None:
            return related_entity
        related_parent_entity = await self._loaded_parent_data(entity=original_parent_entity)
        related_entity.parent = related_parent_entity
        return related_entity

    async def get_relation(self, entity: SingleDepartmentEntity) -> SingleRelationDepartmentDTO:
        logger.info(f"Получениие цепочки в TreeRelatedSingleEntity по id={entity.id}")
        return await self._loaded_parent_data(entity=entity)
