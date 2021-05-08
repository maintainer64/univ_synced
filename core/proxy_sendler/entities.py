from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ResolverEntity:
    base_url: str
    prefix_path: str
    allow_headers_request: Optional[List[str]] = None
    allow_headers_response: Optional[List[str]] = None


@dataclass
class ResponseProxyDTO:
    content: bytes
    headers: dict
    status: int
    url: str
