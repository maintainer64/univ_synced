from typing import Optional

from pydantic import BaseModel, Field


class FacultyEntity(BaseModel):
    id: Optional[int] = Field(None, description="Идентификатор в базе")
    name: str = Field(..., description="Название факультета")

    def update(self, obj: "FacultyEntity") -> "FacultyEntity":
        self.name = obj.name
        return self


class DepartmentEntity(BaseModel):
    id: Optional[int] = Field(None, description="Идентификатор в базе")
    faculty: int = Field(..., description="Идентификатор факультета в базе")
    name: str = Field(..., description="Название департамента")

    def update(self, obj: "DepartmentEntity") -> "DepartmentEntity":
        for field in ("name", "faculty"):
            setattr(self, field, getattr(obj, field))
        return self


class GroupEntity(BaseModel):
    id: Optional[int] = Field(None, description="Идентификатор в базе")
    faculty: int = Field(..., description="Идентификатор факультета в базе")
    department: int = Field(..., description="Идентификатор департамента в базе")
    name: str = Field(..., description="Название группы")

    def update(self, obj: "GroupEntity") -> "GroupEntity":
        for field in ("name", "faculty", "department"):
            setattr(self, field, getattr(obj, field))
        return self
