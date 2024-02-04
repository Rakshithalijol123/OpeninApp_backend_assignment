from fastapi import APIRouter, HTTPException
from .urls import USER_CREATE_PATH
import src.database.interaction as db
from datetime import datetime

from src.models.requests import (
    User, SubTaskModel, PriorityTaskModel, StatusTaskModel, TaskCreate
)
from src.models.responses import (
    UserDataModelResponse
)
router = APIRouter()


@router.post(USER_CREATE_PATH)
def create_task(task: TaskCreate):
    task_data = {"title": task.title, "description": task.description,
                 "due_date": task.due_date, "status": "TODO"}
    result = db.tasks_collection.insert_one(task_data)
    task_data["_id"] = str(result.inserted_id)
    return task_data


@router.post("/create-subtask")
def create_subtask(subtask: SubTaskModel):
    task_id = subtask.task_id
    # Check if the task exists
    task = db.tasks_collection.find_one({"_id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Create a new subtask and return its details
    subtask_data = {"task_id": task_id, "status": 0, "created_at": datetime.utcnow(
    ), "updated_at": datetime.utcnow(), "deleted_at": None}
    result = db.subtasks_collection.insert_one(subtask_data)
    subtask_data["_id"] = result.inserted_id
    return subtask_data
