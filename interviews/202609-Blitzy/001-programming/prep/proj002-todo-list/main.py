from enum import Enum

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

DEFAULT_GET_ITEMS_RESP_LIMIT = 0


class ItemStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Item(BaseModel):
    id: int
    text: str
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
items_db: dict[int, Item] = {}

# counter
next_item_id = 0


class CreateItemRequest(BaseModel):
    text: str


class GetItemsRequest(BaseModel):
    limit: int | None = DEFAULT_GET_ITEMS_RESP_LIMIT


class UpdateItemStatusRequest(BaseModel):
    status: ItemStatus


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: CreateItemRequest) -> Item:
    global next_item_id
    id = next_item_id
    next_item_id += 1  # Or we can use a UUID generator instead, if needed.
    item = Item(id=id, text=payload.text)
    items_db[id] = item
    return item


@app.delete("/items", status_code=status.HTTP_200_OK, response_model=list[Item])
def delete_all_items():
    global items_db
    items_db = {}
    return items_db.values()


@app.delete("/items/{id}", status_code=status.HTTP_200_OK, response_model=list[Item])
def delete_item(id: int) -> list[Item]:
    if id in items_db:
        del items_db[id]
        return items_db.values()
    raise HTTPException(
        status_code=404,
        detail=f"No item found with id={id}",
    )


@app.get("/items", response_model=list[Item])
def get_items(payload: GetItemsRequest | None = None) -> list[Item]:
    limit = payload.limit if payload is not None else DEFAULT_GET_ITEMS_RESP_LIMIT
    if not items_db:
        return []
    if limit == 0:
        return items_db.values()
    if 0 < limit:
        return items_db.values()[:limit]
    raise HTTPException(status_code=422, detail="limit is negative")


@app.get("/items/{id}", status_code=status.HTTP_200_OK, response_model=Item)
def get_item(id: int) -> Item:
    if id in items_db:
        return items_db[id]
    raise HTTPException(
        status_code=404,
        detail=f"No item found with id={id}",
    )


@app.patch("/items/{id}", status_code=status.HTTP_200_OK, response_model=Item)
def update_item_status(id: int, req: UpdateItemStatusRequest) -> Item:
    if id in items_db:
        item = items_db[id]
        item.update_status(req.status)
        return item
    raise HTTPException(
        status_code=404,
        detail=f"No item found with id={id}",
    )


# home page
@app.get("/", response_model=dict)
def root():
    return {"status": "todo list server is up and running."}
