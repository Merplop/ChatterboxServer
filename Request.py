from enum import Enum

class Request:
    class Type(Enum):
        CREATE = 1,
        READ = 2,
        UPDATE = 3,
        DELETE = 4

    def __init__(self, type, content):
        self.type = type
        self.content = content