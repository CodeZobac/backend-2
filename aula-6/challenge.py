import asyncio
import time
from typing import List

class RateLimiter:
    def __init__(self, tasks_per_second: int):
        self.semaphore = asyncio.Semaphore(tasks_per_second)
        self.tasks_per_second = tasks_per_second
        self.last_check = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            current_time = time.time()
            if current_time - self.last_check >= 1:
                # Reset semaphore for the new second
                self.semaphore = asyncio.Semaphore(self.tasks_per_second)
                self.last_check = current_time
        
        await self.semaphore.acquire()

    def release(self):
        self.semaphore.release()

async def rate_limited_task(task_id: int, rate_limiter: RateLimiter) -> str:
    await rate_limiter.acquire()
    try:
        # Simulate some work
        await asyncio.sleep(0.2)
        current_time = time.time()
        return f"Task {task_id} completed at {current_time:.2f}"
    finally:
        rate_limiter.release()

async def main():
    # Allow only 3 tasks per second
    rate_limiter = RateLimiter(tasks_per_second=3)
    
    # Create 10 tasks that will be rate limited
    tasks = [
        asyncio.create_task(rate_limited_task(i, rate_limiter))
        for i in range(10)
    ]
    
    print("Starting rate-limited tasks...")
    results = await asyncio.gather(*tasks)
    
    print("\nResults:")
    for result in results:
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
