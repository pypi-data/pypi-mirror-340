import typing

import pydantic

from gadhttpclient import enums


class HTTPProperty(pydantic.BaseModel):
    name: str
    annotation: str
    location: enums.HTTPAttribute
    required: bool


class HTTPFunction(pydantic.BaseModel):
    arguments: typing.List[HTTPProperty]
    headers: typing.List[HTTPProperty]
    options: typing.Dict[str, typing.Any] = pydantic.Field(default_factory=dict)
