from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
  return {"msg": "Hello world!"}

@app.get("/items/{item_id}")
def items(item_id: int, q: Optional[str] = None):
  return {"item_id": item_id, "q": q}
