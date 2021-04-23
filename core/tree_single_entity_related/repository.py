from abc import ABC, abstractmethod
from typing import Dict
from core.singletable_api.entities import DepartmentEntity as SingleDepartmentEntity
from core.tree_single_entity_related.dto import SingleRelationDepartmentDTO


class TreeRelatedSingleEntityBase(ABC):
    @abstractmethod
    async def set_cache(self, data: Dict[str, SingleDepartmentEntity]):
        ...

    @abstractmethod
    async def get_relation(self, entity: SingleDepartmentEntity) -> SingleRelationDepartmentDTO:
        ...
