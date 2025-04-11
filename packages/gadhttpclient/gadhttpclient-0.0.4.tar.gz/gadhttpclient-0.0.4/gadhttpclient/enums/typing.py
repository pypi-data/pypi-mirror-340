import enum
import typing


class TypingType(str, enum.Enum):
    array = "List"
    union = "Union"
    null = "Optional"
    any = "Any"

    def wrapp(self, annotation: typing.Optional[str] = None) -> str:
        if self in (self.array, self.union):
            return f"{self.value}[{annotation}]"
        elif self is self.null:
            return f"{self.value}[{annotation}] = None"
        else:
            return self.value
