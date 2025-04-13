import enum

class Sql_Status(enum.Enum):
    unconnected: int
    disconnected: int
    connected: int

class Isolation_Status(enum.Enum):
    read_uncommitted: int
    read_committed: int
    repeatable_read: int
    serializable: int

class Commit_Status(enum.Enum):
    manual_commit: int
    auto_commit: int
