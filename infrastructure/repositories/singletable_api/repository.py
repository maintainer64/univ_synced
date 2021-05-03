from logging import getLogger
from typing import List

from aiohttp import ClientResponseError

from core.singletable_api.dto import DepartmentEntity
from core.singletable_api.exceptions import DepartmentNotFound, DepartmentNotCreated, DepartmentNotUpdate
from core.singletable_api.repository import SingletableUniversityApiBase
from infrastructure.repositories.client_template import validators
from infrastructure.repositories.client_template.template import ApiRepository

logger = getLogger(__name__)


class SingletableUniversityApi(SingletableUniversityApiBase, ApiRepository):
    async def departments_get(self) -> List[DepartmentEntity]:
        response = await self._request(method="GET", path="app/departments")
        return validators.validate_list(response=response, base_model=DepartmentEntity)

    async def department_get_by_id(self, identifier: int) -> DepartmentEntity:
        try:
            response = await self._request(method="GET", path="app/departments", params={"id": identifier})
        except ClientResponseError:
            raise DepartmentNotFound
        return validators.validate_dict(response=response, base_model=DepartmentEntity)

    async def department_get_by_ext_id(self, ext_identifier: str) -> DepartmentEntity:
        try:
            response = await self._request(method="GET", path="app/departments", params={"ext-id": ext_identifier})
        except ClientResponseError:
            raise DepartmentNotFound
        return validators.validate_dict(response=response, base_model=DepartmentEntity)

    async def department_create(self, department: DepartmentEntity) -> DepartmentEntity:
        try:
            response = await self._request(method="POST", path="app/departments", json=department.to_dict())
        except ClientResponseError:
            raise DepartmentNotCreated
        return validators.validate_dict(response=response, base_model=DepartmentEntity)

    async def department_update_by_id(self, department: DepartmentEntity) -> DepartmentEntity:
        if department.id is None:
            raise DepartmentNotUpdate
        await self._request(
            method="PUT",
            path="app/departments",
            params={"id": department.id},
            json=department.to_dict(),
            no_response=True,
        )
        return department

    async def department_update_by_ext_id(self, department: DepartmentEntity) -> DepartmentEntity:
        if department.id is None:
            raise DepartmentNotUpdate
        await self._request(
            method="PUT",
            path="app/departments",
            params={"ext-id": department.extId},
            json=department.to_update_by_ext_id(),
            no_response=True,
        )
        return department
