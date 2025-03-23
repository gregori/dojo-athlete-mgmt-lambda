import http
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.v1 import validator, root_validator


class PathParameters(BaseModel):
    id: Optional[str]


class Event(BaseModel):
    resource: str
    path: str
    http_method: http.HTTPMethod = Field(alias="httpMethod")
    headers: dict
    query_parameters: Optional[dict] = Field(alias="queryStringParameters")
    path_parameters: PathParameters = Field(alias="pathParameters")
    body: Optional[str]

    @validator("http_method")
    def validate_http_method(cls, value):
        valid_methods = {
            http.HTTPMethod.GET,
            http.HTTPMethod.POST,
            http.HTTPMethod.PUT,
            http.HTTPMethod.DELETE,
        }
        if value not in valid_methods:
            raise ValueError(
                f"Método HTTP '{value}' não é válido. Apenas GET, POST, PUT ou DELETE são permitidos."
            )
        return value

    @root_validator
    def validate_body(cls, values):
        if values.get("http_method") in {
            http.HTTPMethod.POST,
            http.HTTPMethod.PUT,
        }:
            if not values.get("body"):
                raise ValueError(
                    "Corpo da requisição é obrigatório para as operações POST e PUT."
                )
        return values

    @root_validator
    def validate_path_parameters(cls, values):
        http_method = values.get("http_method")
        path_parameters = values.get("path_parameters")

        if http_method in {
            http.HTTPMethod.GET,
            http.HTTPMethod.PUT,
            http.HTTPMethod.DELETE,
        }:
            if not path_parameters or not path_parameters.id:
                raise ValueError(
                    "Parâmetro 'id' é obrigatório para as operações GET, PUT e DELETE."
                )
        return values
