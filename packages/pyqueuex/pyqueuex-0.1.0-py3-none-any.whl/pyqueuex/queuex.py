import redis.asyncio as redis
import asyncio
import json
import uuid
from typing import Any, Dict, Optional, Callable
from .job import Job, JobOptions
from .worker import Worker
from .strategies import QueueStrategy
from .exceptions import QueueNotFoundError
from .types import RedisConfig

class QueueX:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None
    ):
        """Initialize QueueX with Redis connection parameters."""
        self.redis_config = RedisConfig(host=host, port=port, db=db, password=password)
        self.redis = redis.Redis(
            host=self.redis_config.host,
            port=self.redis_config.port,
            db=self.redis_config.db,
            password=self.redis_config.password,
            decode_responses=True
        )
        self.queues: Dict[str, Dict[str, Any]] = {}
        self.event_handlers: Dict[str, list[Callable]] = {}

    async def create_queue(self, queue_name: str, options: Dict[str, Any] = None) -> str:
        """Create a queue with specified options."""
        options = options or {}
        strategy = options.get("strategy", QueueStrategy.FIFO)
        max_concurrency = options.get("max_concurrency", 1)
        rate_limit = options.get("rate_limit", {})
        self.queues[queue_name] = {
            "strategy": strategy,
            "max_concurrency": max_concurrency,
            "rate_limit": rate_limit
        }
        return queue_name

    async def enqueue(
        self,
        queue_name: str,
        data: Any,
        options: Optional[JobOptions] = None
    ) -> str:
        """Enqueue a job with retry and chaining options."""
        if queue_name not in self.queues:
            raise QueueNotFoundError(f"Queue {queue_name} does not exist")

        options = options or JobOptions()
        job_id = str(uuid.uuid4())
        job = Job(
            id=job_id,
            data=data,
            queue_name=queue_name,
            retries=options.retries,
            backoff=options.backoff,
            timeout=options.timeout,
            ttl=options.ttl,
            priority=options.priority,
            chain=options.chain
        )

        job_data = json.dumps(job.to_dict())
        await self.redis.rpush(f"queuex:{queue_name}", job_data)

        if options.priority:
            await self.redis.zadd(
                f"queuex:{queue_name}:priority",
                {job_data: self._priority_score(options.priority)}
            )

        self._emit("job_queued", job)
        return job_id

    async def start_worker(self, queue_name: str, processor: Callable) -> None:
        """Start a worker to process jobs in the queue."""
        if queue_name not in self.queues:
            raise QueueNotFoundError(f"Queue {queue_name} does not exist")
        worker = Worker(self, queue_name, processor)
        await worker.start()

    def on(self, event: str, handler: Callable) -> None:
        """Register an event handler."""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)

    def _emit(self, event: str, data: Any) -> None:
        """Emit an event to all registered handlers."""
        for handler in self.event_handlers.get(event, []):
            if asyncio.iscoroutinefunction(handler):
                asyncio.create_task(handler(data))
            else:
                handler(data)

    def _priority_score(self, priority: str) -> float:
        """Convert priority to score."""
        return {"high": 3.0, "medium": 2.0, "low": 1.0}.get(priority, 2.0)

    async def close(self) -> None:
        """Close the Redis connection."""
        await self.redis.close()