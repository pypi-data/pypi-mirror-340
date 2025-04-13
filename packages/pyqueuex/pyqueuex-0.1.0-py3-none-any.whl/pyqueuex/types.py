from typing import TypedDict, Optional

class RedisConfig(TypedDict):
    host: str
    port: int
    db: int
    password: Optional[str]

class BackoffConfig(TypedDict):
    type: str
    delay: int
    max_delay: Optional[int]