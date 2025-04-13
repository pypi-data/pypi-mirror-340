from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import time
from .types import BackoffConfig

@dataclass
class Backoff:
    type: str  # 'exponential', 'linear', 'fixed'
    delay: int
    max_delay: Optional[int] = None

    def to_dict(self) -> BackoffConfig:
        return {
            "type": self.type,
            "delay": self.delay,
            "max_delay": self.max_delay
        }

    @classmethod
    def from_dict(cls, data: BackoffConfig) -> "Backoff":
        return cls(**data)

@dataclass
class JobOptions:
    priority: str = "medium"
    retries: int = 0
    backoff: Optional[Backoff] = None
    timeout: Optional[int] = None
    ttl: Optional[int] = None
    delay: Optional[int] = None
    concurrency: Optional[int] = None
    depends_on: Optional[List[str]] = None
    cron: Optional[str] = None
    chain: Optional[List[Dict[str, Any]]] = None

@dataclass
class Job:
    id: str
    data: Any
    queue_name: str
    retries: int = 0
    backoff: Optional[Backoff] = None
    timeout: Optional[int] = None
    ttl: Optional[int] = None
    priority: str = "medium"
    chain: Optional[List[Dict[str, Any]]] = None
    context: Optional[Any] = None
    created_at: float = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "data": self.data,
            "queue_name": self.queue_name,
            "retries": self.retries,
            "backoff": self.backoff.to_dict() if self.backoff else None,
            "timeout": self.timeout,
            "ttl": self.ttl,
            "priority": self.priority,
            "chain": self.chain,
            "context": self.context,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Job":
        data = data.copy()
        if data.get("backoff"):
            data["backoff"] = Backoff.from_dict(data["backoff"])
        return cls(**data)