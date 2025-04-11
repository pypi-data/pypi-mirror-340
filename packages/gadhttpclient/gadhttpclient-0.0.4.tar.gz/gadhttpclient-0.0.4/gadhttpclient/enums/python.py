import enum


class PythonModule(str, enum.Enum):
    pydantic = "pydantic"
    dataclasses = "dataclasses"
    typing = "typing"
    msgspec = "msgspec"


class PythonType(str, enum.Enum):
    object = "dict"
    array = "list"
    string = "str"
    integer = "int"
    number = "float"
    boolean = "bool"
    null = "None"
    bytes = "bytes"
