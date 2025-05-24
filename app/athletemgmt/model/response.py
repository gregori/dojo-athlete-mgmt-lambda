from typing import Optional

from pydantic import BaseModel, Field


class Response(BaseModel):
    status_code: int = Field(serialization_alias="statusCode")
    body: Optional[str]
