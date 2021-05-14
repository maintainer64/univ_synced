import dataclasses

from starlette.requests import Request

from core.proxy_sendler.entities import ResponseProxyDTO
from pydantic import BaseModel, Field
from typing import Optional


@dataclasses.dataclass
class RequestManagerDTO:
    request: Request
    response: ResponseProxyDTO


class DataWithIdDTO(BaseModel):
    id: int


class DataWithIdOrExtIdDTO(BaseModel):
    id: Optional[int] = None
    ext: Optional[str] = Field(None, alias="ext-id")


class UpdateDataDTO(BaseModel):
    query: DataWithIdDTO


class DepartmentUpdateExtDataDTO(BaseModel):
    query: DataWithIdOrExtIdDTO


class CreateDataDTO(BaseModel):
    data: DataWithIdDTO
