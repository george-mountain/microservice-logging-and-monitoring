from fastapi import APIRouter, HTTPException, Request
from prometheus_client import Counter
from pydantic import BaseModel
from typing import List
from utils.logger_config import app_logger
from uuid import uuid4

router = APIRouter()

request_counter = Counter(
    "user_requests_total", "Total number of user requests", ["operation", "status"]
)


class User(BaseModel):
    user_id: int
    username: str


@router.get("/", response_model=List[User])
async def read_users(request: Request):
    """
    Retrieve a list of users.

    Returns:
        List[User]: A list of users.
    """
    log_id = str(uuid4())
    with app_logger.contextualize(log_id=log_id):
        try:
            users = [
                {"user_id": 1, "username": "User One"},
                {"user_id": 2, "username": "User Two"},
            ]
            return users
        except Exception as ex:
            app_logger.error(f"Failed to retrieve users: {ex}")
            request_counter.labels(operation="read", status="error").inc()
            raise HTTPException(status_code=500, detail="Failed to retrieve users")


@router.post("/", response_model=User)
async def create_user(request: Request, user: User):
    """
    Create a new user.

    Args:
        user (User): The user to create.

    Returns:
        User: The created user.
    """
    log_id = str(uuid4())
    with app_logger.contextualize(log_id=log_id):
        try:
            created_user = {"user_id": 3, "username": user.username}
            return created_user
        except Exception as ex:
            app_logger.error(f"Failed to create user: {ex}")
            request_counter.labels(operation="create", status="error").inc()
            raise HTTPException(status_code=500, detail="Failed to create user")
