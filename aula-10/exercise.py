from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    input_text: str

@app.post("/sanitize")
async def sanitize_input(data: InputData):
    sanitized_text = data.input_text.replace("<", "&lt;").replace(">", "&gt;")
    return {"sanitized_text": sanitized_text}
