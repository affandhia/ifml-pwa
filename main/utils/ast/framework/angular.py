from enum import Enum
from ..base import Node

class NodeType(Enum):
    MODEL = 0
    COMPONENT = 1
    SERVICE = 2
    WORKER_FUNCTION = 3

