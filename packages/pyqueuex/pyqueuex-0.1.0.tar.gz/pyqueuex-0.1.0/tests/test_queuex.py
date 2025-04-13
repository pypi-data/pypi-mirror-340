import pytest
import asyncio
from pyqueuex import QueueX, JobOptions, Backoff, QueueStrategy

@pytest.mark.asyncio
async def test_enqueue_and_process():
    queuex = QueueX(host="localhost", port=6379, db=0)
    await queuex.create_queue("test_queue", {"max_concurrency": 1})

    job_data = {"test": "data"}
    job_id = await queuex.enqueue("test_queue", job_data)

    processed = []

    async def processor(job):
        processed.append(job.data)
        return {"result": "success"}

    await queuex.start_worker("test_queue", processor)
    await asyncio.sleep(0.1)

    assert len(processed) == 1
    assert processed[0] == job_data

    await queuex.close()

@pytest.mark.asyncio
async def test_retry_strategy():
    queuex = QueueX(host="localhost", port=6379, db=0)
    await queuex.create_queue("retry_queue")

    job_data = {"test": "retry"}
    await queuex.enqueue(
        "retry_queue",
        job_data,
        JobOptions(
            retries=2,
            backoff=Backoff(type="fixed", delay=100)
        )
    )

    processed = []

    async def processor(job):
        processed.append(job)
        raise Exception("Force retry")

    await queuex.start_worker("retry_queue", processor)
    await asyncio.sleep(0.5)

    assert len(processed) == 3  # Original + 2 retries

    await queuex.close()