import fastapi
import uvicorn

app = fastapi.FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000) 
