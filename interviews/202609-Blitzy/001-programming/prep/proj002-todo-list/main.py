from enum import Enum

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

DEFAULT_LIMIT = 10


class ItemStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Item(BaseModel):
    text: str = None
    status: ItemStatus = ItemStatus.NOT_STARTED

    def update_status(self, new_status: ItemStatus):
        if new_status == ItemStatus.NOT_STARTED or (
            self.status,
            new_status,
        ) not in {
            (ItemStatus.NOT_STARTED, ItemStatus.IN_PROGRESS),
            (ItemStatus.IN_PROGRESS, ItemStatus.DONE),
        }:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail=f"Moving from state {self.status} to {new_status} is not allowed",
            )
        self.status = new_status


# app
app = FastAPI(title="TODO List app")

# db
items_db: list[Item] = []


class UpdateItemStatusRequest(BaseModel):
    status: ItemStatus


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item) -> Item:
    items_db.append(item)
    return items_db[-1]


@app.delete("/items", status_code=status.HTTP_200_OK, response_model=list[Item])
def delete_all_items():
    global items_db
    items_db = []
    return items_db


@app.delete("/items/{id}", status_code=status.HTTP_200_OK, response_model=list[Item])
def delete_item(id: int) -> list[Item]:
    if 0 <= id < len(items_db):
        del items_db[id]
        return items_db
    raise HTTPException(
        status_code=404,
        detail=f"Item-id {id} is not a valid id. There are total {len(items_db)} items right now, and id should be in range [0, {len(items_db)}).",
    )


@app.get("/items", response_model=list[Item])
def get_items(limit: int = DEFAULT_LIMIT, start: int = 0) -> list[Item]:
    if not items_db:
        if start != 0:
            raise HTTPException(
                status_code=422, detail="no items in the list currently"
            )
        if limit != DEFAULT_LIMIT:
            raise HTTPException(
                status_code=422, detail="no items in the list currently"
            )
        return []
    if 0 <= start < len(items_db):
        if limit == 0:
            return items_db[start:]
        if 0 < limit:
            return items_db[start : start + limit]
        raise HTTPException(status_code=422, detail="limit is negative")
    raise HTTPException(status_code=422, detail="start is either negative or too high")


@app.get("/items/{id}", status_code=status.HTTP_200_OK, response_model=Item)
def get_item(id: int) -> Item:
    if 0 <= id < len(items_db):
        return items_db[id]
    raise HTTPException(
        status_code=404,
        detail=f"Item-id {id} is not a valid id. There are total {len(items_db)} items right now, and id should be in range [0, {len(items_db)}).",
    )


@app.patch("/items/{id}", status_code=status.HTTP_200_OK, response_model=Item)
def update_item_status(id: int, req: UpdateItemStatusRequest) -> Item:
    if 0 <= id < len(items_db):
        item = items_db[id]
        item.update_status(req.status)
        return item
    raise HTTPException(
        status_code=404,
        detail=f"Item-id {id} is not a valid id. There are total {len(items_db)} items right now, and id should be in range [0, {len(items_db)}).",
    )


# home page
@app.get("/", response_model=dict)
def root():
    return {"status": "todo list server is up and running."}
