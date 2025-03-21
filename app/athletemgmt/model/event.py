import http
from typing import Optional

from pydantic import BaseModel, Field


class Event(BaseModel):
    resource: str
    path: str
    http_method: http.HTTPMethod = Field(alias="httpMethod")
    headers: dict
    query_parameters: dict = Field(alias="queryStringParameters")
    path_parameters: dict = Field(alias="pathParameters")
    body: Optional[str]