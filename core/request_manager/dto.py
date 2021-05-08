import dataclasses

from starlette.requests import Request

from core.proxy_sendler.entities import ResponseProxyDTO
from pydantic import BaseModel


@dataclasses.dataclass
class RequestManagerDTO:
    request: Request
    response: ResponseProxyDTO


class DataWithIdDTO(BaseModel):
    id: int


class UpdateDataDTO(BaseModel):
    query: DataWithIdDTO


class CreateDataDTO(BaseModel):
    data: DataWithIdDTO
