from enum import Enum
from ..base import Node

class NodeType(Enum):
    TEXT = 0
    VAR = 1
    FUNCTION = 2
    CLASS = 3
    COMMENT = 4
