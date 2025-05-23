# FastAPI Hello World Application
from fastapi import FastAPI

app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI application following best practices",
    version="1.0.0"
)

@app.get("/")
async def index():
    """Hello World endpoint following REST conventions"""
    return {"message": "Hello from FastAPI"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
