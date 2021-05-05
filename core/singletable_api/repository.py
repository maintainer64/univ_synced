from abc import ABC, abstractmethod
from typing import List

from core.singletable_api.entities import DepartmentEntity


class SingletableUniversityApiBase(ABC):
    @abstractmethod
    async def departments_get(self) -> List[DepartmentEntity]:
        ...

    @abstractmethod
    async def department_get_by_id(self, identifier: int) -> DepartmentEntity:
        """
        :raises: DepartmentNotFound
        """
        ...

    @abstractmethod
    async def department_get_by_ext_id(self, ext_identifier: str) -> DepartmentEntity:
        """
        :raises: DepartmentNotFound
        """
        ...

    @abstractmethod
    async def department_create(self, department: DepartmentEntity) -> DepartmentEntity:
        """
        :raises: DepartmentNotCreated
        """
        ...

    @abstractmethod
    async def department_update_by_id(self, department: DepartmentEntity) -> DepartmentEntity:
        """
        :raises: DepartmentNotUpdate
        """
        ...

    @abstractmethod
    async def department_update_by_ext_id(self, department: DepartmentEntity) -> DepartmentEntity:
        """
        :raises: DepartmentNotUpdate
        """
        ...
