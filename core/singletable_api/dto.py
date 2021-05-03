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
