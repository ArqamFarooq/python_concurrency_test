import asyncio
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from threading import Lock
from statistics import mean

app = FastAPI()
numbers = []
lock = Lock()

class NumberPayload(BaseModel):
    number: int

@app.post("/numbers")
async def add_number(payload: NumberPayload):
    with lock:
        numbers.append(payload.number)
    return {"status": "success", "number": payload.number}

@app.get("/average")
async def get_average():
    with lock:
        if not numbers:
            raise HTTPException(status_code=404, detail="No numbers submitted")
        avg = mean(numbers)
    return {"average": avg}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)