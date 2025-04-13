import enum
from _typeshed import Incomplete

class NtsuQueryError(Exception): ...

class query_type(enum.Enum):
    SteamAPI: int
    A2S: int

class n_valveServerQuery:
    class server_info:
        server_ip: Incomplete
        server_port: Incomplete
        server_name: Incomplete
        server_transname: Incomplete
        server_onlineplayer_count: Incomplete
        server_maxplayer_count: Incomplete
        server_mapname: Incomplete
        game: Incomplete
        timeout: Incomplete
        gametype: Incomplete
        querystatus: Incomplete
        def __init__(self, server_ip: str, server_port: int, server_name: str = ..., server_onlineplayer_count: int = ..., server_maxplayer_count: int = ..., server_mapname: str = ..., game: str = ..., timeout: int = ..., gametype: Incomplete | None = ..., querystatus: bool = ...) -> None: ...
        def is_error(self): ...
    timeout: Incomplete
    retrytimes: Incomplete
    encoding: Incomplete
    header: Incomplete
    session: Incomplete
    steamwebapikey: Incomplete
    def __init__(self, timeout: float, encoding: str, steamwebapikey: str, retrytimes: int = ...) -> None: ...
    @classmethod
    def resolve_domain_to_ip(cls, domain): ...
    def query_servers(self, addresses: list, q_type: query_type, max_workers: int = ..., group: int = ..., interval: float = ...) -> list[server_info]: ...
