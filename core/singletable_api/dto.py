from typing import Optional

from pydantic import BaseModel, Field


class DepartmentEntity(BaseModel):
    id: Optional[int] = Field(None, description="Идентификатор в базе")
    name: str = Field(..., description="Название департамента")
    extId: str = Field(..., description="Идентификатор департамента в внешней базе")
    parentExtId: Optional[str] = Field(None, description="Родительский элемент в внешней базе")

    def to_dict(self):
        data = self.dict(exclude={"id", "parentExtId"})
        if self.parentExtId:
            data["parentExtId"] = self.parentExtId
        return data

    def to_update_by_ext_id(self):
        data = self.dict(exclude={"id"})
        if self.parentExtId:
            data["parentExtId"] = self.parentExtId
        return data

    def update(self, obj: "DepartmentEntity") -> "DepartmentEntity":
        for field in ("name", "extId", "parentExtId"):
            setattr(self, field, getattr(obj, field))
        return self
