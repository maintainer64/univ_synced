from abc import ABC, abstractmethod
from typing import Union, Callable, Dict, Optional
from dataclasses import dataclass

from core.any_migration.application.repository import AnySaver, AnyCaster
from core.multitable_api.entities import FacultyEntity, DepartmentEntity, GroupEntity
from core.singletable_api.entities import DepartmentEntity as SingleDepartmentEntity


class MultiFacadeRepositoryBase(
    AnySaver[Union[FacultyEntity, DepartmentEntity, GroupEntity]],
    AnyCaster[SingleDepartmentEntity, Optional[Union[FacultyEntity, DepartmentEntity, GroupEntity]]],
    ABC,
):
    @abstractmethod
    async def set_cache(self, data: Dict[str, SingleDepartmentEntity]):
        ...


@dataclass
class FunctionDTO:
    create: Callable
    update: Callable
    get: Callable
