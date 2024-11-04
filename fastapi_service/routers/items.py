from fastapi import APIRouter, HTTPException, Request
from prometheus_client import Counter
from pydantic import BaseModel
from typing import List
from utils.logger_config import app_logger
from uuid import uuid4

router = APIRouter()

request_counter = Counter(
    "item_requests_total", "Total number of item requests", ["operation", "status"]
)


class Item(BaseModel):
    item_id: int
    name: str


@router.get("/", response_model=List[Item])
async def read_items(request: Request):
    """
    Retrieve a list of items.
    """
    log_id = str(uuid4())
    with app_logger.contextualize(log_id=log_id):
        try:
            items = [
                {"item_id": 1, "name": "Item One"},
                {"item_id": 2, "name": "Item Two"},
            ]
            return items
        except Exception as ex:
            app_logger.error(f"Failed to retrieve items: {ex}")
            request_counter.labels(operation="read", status="error").inc()
            raise HTTPException(status_code=500, detail="Failed to retrieve items")


@router.post("/", response_model=Item)
async def create_item(request: Request, item: Item):
    """
    Create a new item.

    Args:
        item (Item): The item to create.

    Returns:
        Item: The created item.
    """
    log_id = str(uuid4())
    with app_logger.contextualize(log_id=log_id):
        try:
            created_item = {"item_id": 3, "name": item.name}
            return created_item
        except Exception as ex:
            app_logger.error(f"Failed to create item: {ex}")
            request_counter.labels(operation="create", status="error").inc()
            raise HTTPException(status_code=500, detail="Failed to create item")
