from abc import ABC, abstractmethod
from typing import List

from core.multitable_api.entities import DepartmentEntity, FacultyEntity, GroupEntity


class MultitableUniversityApiBase(ABC):
    @abstractmethod
    async def faculties_get(self) -> List[FacultyEntity]:
        ...

    @abstractmethod
    async def faculty_get(self, identifier: int) -> FacultyEntity:
        ...

    @abstractmethod
    async def faculty_create(self, faculty: FacultyEntity) -> FacultyEntity:
        ...

    @abstractmethod
    async def faculty_update(self, faculty: FacultyEntity) -> FacultyEntity:
        ...

    @abstractmethod
    async def departments_get(self) -> List[DepartmentEntity]:
        ...

    @abstractmethod
    async def department_get(self, identifier: int) -> DepartmentEntity:
        ...

    @abstractmethod
    async def department_create(self, department: DepartmentEntity) -> DepartmentEntity:
        ...

    @abstractmethod
    async def department_update(self, department: DepartmentEntity) -> DepartmentEntity:
        ...

    @abstractmethod
    async def groups_get(self) -> List[GroupEntity]:
        ...

    @abstractmethod
    async def group_get(self, identifier: int) -> GroupEntity:
        ...

    @abstractmethod
    async def group_create(self, group: GroupEntity) -> GroupEntity:
        ...

    @abstractmethod
    async def group_update(self, group: GroupEntity) -> GroupEntity:
        ...
