from logging import getLogger
from typing import List

from aiohttp import ClientResponseError

from core.multitable_api.entities import DepartmentEntity, FacultyEntity, GroupEntity
from core.multitable_api.exceptions import DepartmentEntityNotFound, FacultyEntityNotFound, GroupEntityNotFound
from core.multitable_api.repository import MultitableUniversityApiBase
from infrastructure.repositories.client_template import validators
from infrastructure.repositories.client_template.template import ApiRepository

logger = getLogger(__name__)


class MultitableUniversityApi(MultitableUniversityApiBase, ApiRepository):
    async def faculties_get(self) -> List[FacultyEntity]:
        response = await self._request(method="GET", path="app/faculties")
        return validators.validate_list(response=response, base_model=FacultyEntity)

    async def faculty_get(self, identifier: int) -> FacultyEntity:
        try:
            response = await self._request(method="GET", path="app/faculties", params={"id": identifier})
        except ClientResponseError:
            raise FacultyEntityNotFound
        return validators.validate_dict(response=response, base_model=FacultyEntity)

    async def faculty_create(self, faculty: FacultyEntity) -> FacultyEntity:
        response = await self._request(method="POST", path="app/faculties", json=faculty.dict(exclude={"id"}))
        return validators.validate_dict(response=response, base_model=FacultyEntity)

    async def faculty_update(self, faculty: FacultyEntity) -> FacultyEntity:
        await self._request(
            method="PUT",
            path="app/faculties",
            params={"id": faculty.id},
            json=faculty.dict(exclude={"id"}),
            no_response=True,
        )
        return faculty

    async def departments_get(self) -> List[DepartmentEntity]:
        response = await self._request(method="GET", path="app/deps")
        return validators.validate_list(response=response, base_model=DepartmentEntity)

    async def department_get(self, identifier: int) -> DepartmentEntity:
        try:
            response = await self._request(method="GET", path="app/deps", params={"id": identifier})
        except ClientResponseError:
            raise DepartmentEntityNotFound
        return validators.validate_dict(response=response, base_model=DepartmentEntity)

    async def department_create(self, department: DepartmentEntity) -> DepartmentEntity:
        response = await self._request(method="POST", path="app/deps", json=department.dict(exclude={"id"}))
        return validators.validate_dict(response=response, base_model=DepartmentEntity)

    async def department_update(self, department: DepartmentEntity) -> DepartmentEntity:
        await self._request(
            method="PUT",
            path="app/deps",
            params={"id": department.id},
            json=department.dict(exclude={"id"}),
            no_response=True,
        )
        return department

    async def groups_get(self) -> List[GroupEntity]:
        response = await self._request(method="GET", path="app/groups")
        return validators.validate_list(response=response, base_model=GroupEntity)

    async def group_get(self, identifier: int) -> GroupEntity:
        try:
            response = await self._request(method="GET", path="app/groups", params={"id": identifier})
        except ClientResponseError:
            raise GroupEntityNotFound
        return validators.validate_dict(response=response, base_model=GroupEntity)

    async def group_create(self, group: GroupEntity) -> GroupEntity:
        response = await self._request(method="POST", path="app/groups", json=group.dict(exclude={"id"}))
        return validators.validate_dict(response=response, base_model=GroupEntity)

    async def group_update(self, group: GroupEntity) -> GroupEntity:
        await self._request(
            method="PUT", path="app/groups", params={"id": group.id}, json=group.dict(exclude={"id"}), no_response=True,
        )
        return group
