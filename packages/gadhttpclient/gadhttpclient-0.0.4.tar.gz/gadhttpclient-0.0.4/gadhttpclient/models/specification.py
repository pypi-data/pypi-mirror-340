"""
Specification
├── openapi
├── info
│   ├── title
│   ├── description
│   └── version
├── paths
│   ├── <path>
│   │   ├── get
│   │   ├── post
│   │   ├── put
│   │   ├── patch
│   │   └── delete
│   │       ├── tags
│   │       ├── summary
│   │       ├── operationId
│   │       ├── parameters
│   │       │   ├── name
│   │       │   ├── in
│   │       │   ├── required
│   │       │   ├── description
│   │       │   └── schema
│   │       │       └── Schema | Reference
│   │       ├── requestBody
│   │       │   ├── required
│   │       │   └── content
│   │       │       └── <content-type>
│   │       │           └── schema
│   │       │               └── Schema | Reference
│   │       ├── responses
│   │       │   ├── <status-code>
│   │       │   │   ├── description
│   │       │   │   └── content
│   │       │   │       └── <content-type>
│   │       │   │           └── schema
│   │       │   │               └── Schema | Reference
│   │       └── security
├── components
│   └── schemas
│       └── <name>
│           ├── title
│           ├── type
│           ├── format
│           ├── enum
│           ├── description
│           ├── default
│           ├── properties
│           │   └── <name>: Schema | Reference
│           ├── required
│           ├── items
│           │   └── Schema | Reference
│           ├── allOf | anyOf | oneOf
│           │   └── List[Schema | Reference]
│           └── additionalProperties
│               └── bool | Schema | Reference
└── security
"""

from __future__ import annotations

import http
import typing

import pydantic

from gadhttpclient import const
from gadhttpclient import enums


class SpecificationReference(pydantic.BaseModel):
    ref: str = pydantic.Field(..., alias="$ref")

    @classmethod
    def name(cls, value: str) -> str:
        return value.split(const.SYMBOL_FORWARD_SLASH)[-1]


class SpecificationSchema(pydantic.BaseModel):
    title: typing.Optional[str] = None
    type: typing.Optional[enums.SpecificationSchemaType] = None
    format: typing.Optional[enums.SpecificationSchemaFormat] = None
    enum: typing.Optional[typing.List[typing.Any]] = None
    description: typing.Optional[str] = None
    default: typing.Optional[typing.Any] = None
    properties: typing.Optional[typing.Dict[str, typing.Union[SpecificationSchema, SpecificationReference]]] = None
    required: typing.Optional[typing.List[str]] = None
    items: typing.Optional[
        typing.Union[
            SpecificationSchema,
            SpecificationReference,
            typing.List[typing.Union[SpecificationSchema, SpecificationReference]],
        ]
    ] = None
    allOf: typing.Optional[typing.List[typing.Union[SpecificationSchema, SpecificationReference]]] = None
    anyOf: typing.Optional[typing.List[typing.Union[SpecificationSchema, SpecificationReference]]] = None
    oneOf: typing.Optional[typing.List[typing.Union[SpecificationSchema, SpecificationReference]]] = None
    additionalProperties: typing.Optional[typing.Union[bool, SpecificationSchema, SpecificationReference]] = None


class SpecificationContent(pydantic.BaseModel):
    model: typing.Optional[typing.Union[SpecificationSchema, SpecificationReference]] = pydantic.Field(
        None, alias="schema"
    )


class SpecificationPathOperationParameter(pydantic.BaseModel):
    name: str
    location: enums.HTTPAttribute = pydantic.Field(..., alias="in")
    required: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    model: typing.Optional[typing.Union[SpecificationSchema, SpecificationReference]] = pydantic.Field(
        ..., alias="schema"
    )


class SpecificationPathOperationRequestBody(pydantic.BaseModel):
    required: typing.Optional[bool] = None
    content: typing.Dict[enums.HTTPContentType, SpecificationContent]


class SpecificationPathOperationResponse(pydantic.BaseModel):
    description: typing.Optional[str] = None
    content: typing.Optional[typing.Dict[enums.HTTPContentType, SpecificationContent]] = None


class SpecificationPathOperation(pydantic.BaseModel):
    tags: typing.Optional[typing.List[str]] = None
    summary: typing.Optional[str] = None
    operationId: str
    parameters: typing.Optional[
        typing.List[typing.Union[SpecificationPathOperationParameter, SpecificationReference]]
    ] = None
    requestBody: typing.Optional[typing.Union[SpecificationPathOperationRequestBody, SpecificationReference]] = None
    responses: typing.Dict[http.HTTPStatus, SpecificationPathOperationResponse]
    security: typing.Optional[typing.List[typing.Dict[enums.SpecificationSecurityType, typing.List[str]]]] = None


class SpecificationPath(pydantic.BaseModel):
    get: typing.Optional[SpecificationPathOperation] = None
    post: typing.Optional[SpecificationPathOperation] = None
    put: typing.Optional[SpecificationPathOperation] = None
    patch: typing.Optional[SpecificationPathOperation] = None
    delete: typing.Optional[SpecificationPathOperation] = None


class SpecificationInfo(pydantic.BaseModel):
    title: str
    description: typing.Optional[str] = None
    version: str


class SpecificationComponents(pydantic.BaseModel):
    schemas: typing.Optional[typing.Dict[str, typing.Union[SpecificationSchema, SpecificationReference]]] = None


class Specification(pydantic.BaseModel):
    openapi: str
    info: SpecificationInfo
    paths: typing.Dict[str, SpecificationPath]
    components: typing.Optional[SpecificationComponents] = None
    security: typing.Optional[typing.List[typing.Dict[enums.SpecificationSecurityType, typing.List[str]]]] = None
