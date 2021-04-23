from core.singletable_api.entities import DepartmentEntity as SingleDepartmentEntity
from typing import Optional


class SingleRelationDepartmentDTO(SingleDepartmentEntity):
    parent: Optional["SingleRelationDepartmentDTO"]

    def set_parent(self, parent: "SingleRelationDepartmentDTO"):
        self.parent = parent
        return self

    @property
    def level(self):
        return 1 + self.parent.level if self.parent else 0
