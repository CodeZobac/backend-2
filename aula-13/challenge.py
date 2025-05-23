# Refactored FastAPI application with enhanced error handling, logging, and performance
import logging
import asyncio
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Enhanced API",
    description="Refactored application with best practices",
    version="2.0.0"
)

# Add middleware for performance and security
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware for logging and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log response
        logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return {"error": exc.detail, "status_code": exc.status_code}

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return {"error": "Internal server error", "status_code": 500}

@app.get("/")
async def enhanced_index():
    """Enhanced hello world with async processing"""
    # Simulate async processing
    await asyncio.sleep(0.1)
    return {"message": "Hello from Enhanced FastAPI", "version": "2.0.0"}

@app.get("/process/{item_id}")
async def process_item(item_id: int):
    """Example endpoint with error handling and validation"""
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Item ID must be positive")
    
    # Simulate async processing
    await asyncio.sleep(0.2)
    
    return {
        "item_id": item_id,
        "processed": True,
        "timestamp": time.time()
    }

@app.get("/health")
async def health_check():
    """Enhanced health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        access_log=True
    )
