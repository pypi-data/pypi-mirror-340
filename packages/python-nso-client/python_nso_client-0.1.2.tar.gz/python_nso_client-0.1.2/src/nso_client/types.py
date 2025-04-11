from enum import Enum
from typing import TypeAlias


class ContentType(str, Enum):
    YANG_DATA = "application/yang-data+json"
    YANG_PATCH = "application/yang-patch+json"


class PatchType(str, Enum):
    PLAIN = "plain"
    YANG_PATCH = "yang-patch"


class InsertWhere(str, Enum):
    FIRST = "first"
    LAST = "last"
    BEFORE = "before"
    AFTER = "after"


YangData: TypeAlias = (
    None | bool | int | float | str | list["YangData"] | dict[str, "YangData"]
)


class DryRunType(str, Enum):
    CLI = "cli"
    XML = "xml"
    NATIVE = "NATIVE"
