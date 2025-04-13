import redis.asyncio as redis
import asyncio
import json
import time
from typing import Any, Callable, Optional
from .queuex import QueueX
from .job import Job
from .strategies import QueueStrategy
from .exceptions import JobProcessingError

class Worker:
    def __init__(self, queuex: QueueX, queue_name: str, processor: Callable):
        self.queuex = queuex
        self.queue_name = queue_name
        self.processor = processor
        self.running = False

    async def start(self) -> None:
        """Start processing jobs."""
        self.running = True
        queue_config = self.queuex.queues.get(self.queue_name, {})
        strategy = queue_config.get("strategy", QueueStrategy.FIFO)

        while self.running:
            job_data = await self._fetch_job(strategy)
            if job_data:
                await self._process_job(job_data)
            else:
                await asyncio.sleep(0.1)  # Prevent tight loop

    async def _fetch_job(self, strategy: QueueStrategy) -> Optional[Dict[str, Any]]:
        """Fetch a job based on queue strategy."""
        if strategy == QueueStrategy.FIFO:
            job_data = await self.queuex.redis.lpop(f"queuex:{self.queue_name}")
        elif strategy == QueueStrategy.LIFO:
            job_data = await self.queuex.redis.rpop(f"queuex:{self.queue_name}")
        elif strategy == QueueStrategy.PRIORITY:
            result = await self.queuex.redis.zpopmax(f"queuex:{self.queue_name}:priority")
            job_data = result[0] if result else None
        elif strategy == QueueStrategy.ROUND_ROBIN:
            job_data = await self.queuex.redis.lpop(f"queuex:{self.queue_name}")
        else:
            job_data = None

        return json.loads(job_data) if job_data else None

    async def _process_job(self, job_data: Dict[str, Any]) -> None:
        """Process a single job with retries and chaining."""
        job = Job.from_dict(job_data)
        self.queuex._emit("job_started", job)

        try:
            timeout = job.timeout or 60
            async with asyncio.timeout(timeout):
                result = await self.processor(job)
                job.context = result
                self.queuex._emit("job_completed", job)

                # Handle job chaining
                if job.chain:
                    for chained_job in job.chain:
                        chained_data = chained_job["data"]
                        chained_options_data = chained_job.get("options", {})
                        chained_options = JobOptions(**chained_options_data)
                        await self.queuex.enqueue(
                            self.queue_name,
                            chained_data,
                            chained_options
                        )

        except asyncio.TimeoutError:
            self.queuex._emit("job_failed", job)
            await self._handle_retry(job)
        except Exception as e:
            self.queuex._emit("job_failed", job)
            await self._handle_retry(job)

    async def _handle_retry(self, job: Job) -> None:
        """Handle job retry logic."""
        if job.retries > 0:
            job.retries -= 1
            delay = self._calculate_backoff(job)
            job.created_at = time.time() + delay
            self.queuex._emit("job_delayed", job)
            await asyncio.sleep(delay)
            await self.queuex.redis.rpush(
                f"queuex:{self.queue_name}",
                json.dumps(job.to_dict())
            )

    def _calculate_backoff(self, job: Job) -> int:
        """Calculate retry delay based on backoff strategy."""
        if not job.backoff:
            return 0

        if job.backoff.type == "fixed":
            return job.backoff.delay
        elif job.backoff.type == "linear":
            return job.backoff.delay
        elif job.backoff.type == "exponential":
            delay = job.backoff.delay * (2 ** (job.retries + 1))
            return min(delay, job.backoff.max_delay or float("inf"))
        return 0