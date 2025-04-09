from fastapi import FastAPI
import asyncio
import random

app = FastAPI()

async def fetch_from_source_1():
    # Simulate API call delay
    await asyncio.sleep(random.uniform(0.1, 0.5))
    return {"source": "API 1", "data": "Data from source 1"}

async def fetch_from_source_2():
    # Simulate API call delay
    await asyncio.sleep(random.uniform(0.1, 0.5))
    return {"source": "API 2", "data": "Data from source 2"}

@app.get("/combined-data")
async def get_combined_data():
    # Use asyncio.gather to fetch data from both sources concurrently
    result1, result2 = await asyncio.gather(
        fetch_from_source_1(),
        fetch_from_source_2()
    )
    return {
        "source1_data": result1,
        "source2_data": result2
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
