from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str
    is_done: bool = False

items = []

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items", response_model=list[Item])
def list_items(limit: int = Query(10, ge=1, le=100)):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if 0 <= item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")