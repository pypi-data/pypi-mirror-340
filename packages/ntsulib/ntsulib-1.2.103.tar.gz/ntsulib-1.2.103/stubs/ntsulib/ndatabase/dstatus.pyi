from enum import Enum

class Sql_Status(Enum):
    unconnected: int
    disconnected: int
    connected: int

class Isolation_Status(Enum):
    read_uncommitted: int
    read_committed: int
    repeatable_read: int
    serializable: int

class Commit_Status(Enum):
    manual_commit: int
    auto_commit: int
