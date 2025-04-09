import asyncio
from typing import List
import random

async def task_with_random_delay(task_id: int) -> str:
    delay = random.uniform(0.5, 3.0)
    try:
        await asyncio.sleep(delay)
        return f"Task {task_id} completed after {delay:.2f}s"
    except asyncio.CancelledError:
        return f"Task {task_id} was cancelled"

async def run_tasks_with_timeout(timeout: float = 2.0) -> List[str]:
    # Create multiple tasks
    tasks = [
        asyncio.create_task(task_with_random_delay(i))
        for i in range(5)
    ]
    
    results = []
    
    try:
        # Wait for all tasks with timeout
        completed_tasks = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True),
            timeout=timeout
        )
        results.extend(completed_tasks)
    except asyncio.TimeoutError:
        print(f"Timeout occurred after {timeout}s")
        # Cancel any remaining tasks
        for task in tasks:
            if not task.done():
                task.cancel()
        # Wait for cancelled tasks to finish
        remaining = await asyncio.gather(*[t for t in tasks if not t.done()], 
                                       return_exceptions=True)
        results.extend(remaining)
    
    return results

async def main():
    print("Starting tasks with 2 second timeout...")
    results = await run_tasks_with_timeout()
    print("\nResults:")
    for result in results:
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
