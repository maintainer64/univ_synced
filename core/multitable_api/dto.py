from pydantic import BaseModel, Field


class FacultyEntity(BaseModel):
    id: int = Field(None, description="Идентификатор в базе")
    name: str = Field(..., description="Название факультета")


class DepartmentEntity(BaseModel):
    id: int = Field(None, description="Идентификатор в базе")
    faculty: int = Field(..., description="Идентификатор факультета в базе")
    name: str = Field(..., description="Название департамента")


class GroupEntity(BaseModel):
    id: int = Field(None, description="Идентификатор в базе")
    faculty: int = Field(..., description="Идентификатор факультета в базе")
    department: int = Field(..., description="Идентификатор департамента в базе")
    name: str = Field(..., description="Название группы")
