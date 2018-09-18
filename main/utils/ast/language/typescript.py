from enum import Enum

class NodeType(Enum):
    TEXT = 0
    VAR = 1
    FUNCTION = 2
    CLASS = 3
    COMMENT = 4

class Node(object):
    id = None

    def render(self):
        pass
