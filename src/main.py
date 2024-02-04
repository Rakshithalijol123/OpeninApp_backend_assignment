# Fastapi imports here.
from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone
from typing import List, Optional
# from dateutil import parser

# Any other imports which are not related to fastapi.
import os

# Folder based imports here
from src.utils.auth import (
    authenticate_user,
    validate_token
)

from src.config import (
    APP_NAME,
    APP_DESCRIPTION
)

from src.utils.openapi import (
    _patch_http_validation_error
)
from src.apps.exceptions.exception import (
    handle_validation_exception,
    handle_http_exception,
    handle_unexpected_exception)
from src.apps.endpoints.views import router as endpoints_router


# Intialise a instance of a FastAPI with proper conventions.
app = FastAPI(title=APP_NAME, description=APP_DESCRIPTION)
app.openapi = _patch_http_validation_error(app, app.openapi)

# Permissions for CORS when app running locally.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---Handle exceptions ---
app.add_exception_handler(StarletteHTTPException, handle_http_exception)
app.add_exception_handler(Exception, handle_unexpected_exception)
app.add_exception_handler(RequestValidationError, handle_validation_exception)
SWAGGER_ENDPOINT = os.getenv("SWAGGER_ENDPOINT", "/docs")


@app.get("/", include_in_schema=False)
def redirect_to_swagger():
    """Redirect to Swagger UI when accessing the root endpoint"""
    return RedirectResponse(SWAGGER_ENDPOINT)

# --- END-POINTS ---


@app.post("/oauth/token", include_in_schema=False)
def token(formData: OAuth2PasswordRequestForm = Depends()):
    access_token = authenticate_user(formData.username, formData.password)
    if access_token is not None:
        return {"access_token": access_token}
    raise HTTPException(
        status_code=401,
        detail={
            "title": "Authorization Header Missing",
            "details": "Authorization token not found in request header",
            "status": 401,
        },
    )


# app.include_router(endpoints_router)
# dependencies=[Depends(validate_token)]

class UserDBModel(BaseModel):
    id: int
    phone_number: int
    priority: int


class SubTaskDBModel(BaseModel):
    id: int
    task_id: int
    status: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

# SUBTASK TABLE:
#     id ,task_id, status (0,1), created_at,updated_at, deleted_at


class TaskDBModel(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    priority: int
    status: str = "TODO"
    user_id: int
    updated_at: datetime = None
    deleted_at: datetime = None


DATABASE_URL = "mongodb://localhost:27017"
client = MongoClient(DATABASE_URL)
db = client["your_database_name"]
test_user = db["Test_user"]
test_task = db["Test_task"]
test_subtask = db["Test_subtask"]


@app.post("/create-task", summary="Task Creation", tags=["Task creation"])
def create_task(task: TaskDBModel, dependencies: list = Depends(validate_token)):
    try:
        task_dict = task.dict()
        task_dict["priority"] = get_priority(task_dict.get("due_date"))
        task_dict["deleted_at"] = None
        task_dict["updated_at"] = None
        check_task_already_exist = test_task.find_one(
            {"id": task_dict.get("id"), "deleted_at": {"$eq": None}})
        if check_task_already_exist is None:
            print(f"****************{task_dict}")
            result = test_task.insert_one(task_dict)
            return {"id": str(result.inserted_id)}
        else:
            return {"Status": "id is already exists"}
    except Exception as e:
        print(f"***************{e}**************")


# @app.post("/create-subtask/{task_id}")
# def create_subtask(task_id: int, subtask: SubTaskDBModel):
#     # Implement your logic to insert subtask into MongoDB
#     task = test_task.find_one({"id": task_id})
#     if task:
#         subtask_dict = subtask.dict()
#         subtask_dict["task_id"] = task_id
#         subtask_dict["created_at"] = datetime.utcnow()
#         subtask_id = str(test_subtask.insert_one(subtask_dict).inserted_id)
#         return {"id": subtask_id}
#     else:
#         raise HTTPException(status_code=404, detail="Task not found")

@app.post("/create-subtask/{task_id}", tags=["Task creation"])
def create_subtask(task_id: int):
    # Implement your logic to insert subtask into MongoDB
    total_subtasks = len(
        list(test_subtask.find({"deleted_at": {"$eq": None}})))
    subtask_dict = dict()
    task = test_task.find_one({"id": task_id, "deleted_at": {"$eq": None}})
    if task:
        subtask_dict["id"] = total_subtasks + 1
        subtask_dict["task_id"] = task_id
        subtask_dict["created_at"] = datetime.utcnow()
        subtask_dict["updated_at"] = None
        subtask_dict["deleted_at"] = None
        subtask_dict["status"] = 0
        subtask_id = str(test_subtask.insert_one(subtask_dict).inserted_id)
        update_task_status(task_id)
        return {"id": subtask_id}
    else:
        raise HTTPException(status_code=404, detail="Task not found")

# SUBTASK TABLE:
#     id ,task_id, status (0,1), created_at,updated_at, deleted_at


def update_task_status(task_id: int):
    r1 = len(list(test_subtask.find(
        {"task_id": task_id, "status": 1, "deleted_at": {"$eq": None}})))
    r2 = len(list(test_subtask.find(
        {"task_id": task_id, "deleted_at": {"$eq": None}})))
    if r1 == r2:
        # status of task = DONE
        test_task.update_one({"id": task_id, "deleted_at": {"$eq": None}}, {
                             "$set": {"status": "DONE", "updated_at": datetime.utcnow()}})

    elif r1 >= 1:
        # status of task = IN_PROGRESS
        test_task.update_one(
            {"id": task_id, "deleted_at": {"$eq": None}}, {"$set": {"status": "IN_PROGRESS",  "updated_at": datetime.utcnow()}})
    else:
        test_task.update_one(
            {"id": task_id, "deleted_at": {"$eq": None}}, {"$set": {"status": "TODO", "updated_at": datetime.utcnow()}})


@app.post("/register-user", tags=["User creation"])
def user_register(user: UserDBModel):
    user = dict(user)
    user_data = test_user.insert_one(user)
    return {"id": str(user_data.inserted_id)}


@app.patch("/update-subtask", tags=["Task Updation"])
def update_subtask(subtask_id: int, status: int):
    # check = list(test_subtask.find_one({"id": subtask_id}))
    # print(check)
    updated_subtask_status = test_subtask.update_one(
        {"id": subtask_id, "deleted_at": {"$eq": None}}, {"$set": {"status": status, "updated_at": datetime.utcnow()}})
    # print()
    # subtask_dict = dict()
    subtasks = (test_subtask.find_one(
        {"id": subtask_id, "deleted_at": {"$eq": None}}))
    # print(subtasks.get("id"))
    # print(subtask_dict)
    update_task_status(subtasks.get("task_id"))
    return {"Count": updated_subtask_status.modified_count}


@app.patch("/update-task", tags=["Task Updation"])
def update_task(task_id: int, due_date: datetime, status: str):
    # check = list(test_subtask.find_one({"id": subtask_id}))
    # print(check)
    updated_task_status = test_task.update_one(
        {"id": task_id, "deleted_at": {"$eq": None}}, {"$set": {"status": status, "due_date": due_date, "updated_at": datetime.utcnow(), "priority": get_priority(due_date)}})
    if status == "DONE":
        updated_subtask_status = test_subtask.update_many(
            {"task_id": task_id, "deleted_at": {"$eq": None}}, {"$set": {"status": 1, "updated_at": datetime.utcnow()}})
        print(updated_subtask_status.modified_count)
    elif status == "TODO":
        updated_subtask_status = test_subtask.update_many(
            {"task_id": task_id, "deleted_at": {"$eq": None}}, {"$set": {"status": 0, "updated_at": datetime.utcnow()}})
        print(updated_subtask_status.modified_count)
        # print(list(updated_subtask_status))
    return {"Count": updated_task_status.modified_count}


def get_priority(due_date):
    current_date_utc_aware = datetime.now(timezone.utc)
    difference = (due_date - current_date_utc_aware).days

    if difference <= 0:
        return 0
    elif 0 < difference <= 2:
        return 1
    elif 2 < difference <= 4:
        return 2
    else:
        return 3


@app.patch("/delete-task", tags=["Task Deletion"])
def delete_task(task_id: int):
    update_deleted_at = test_task.update_one(
        {"id": task_id, "deleted_at": {"$eq": None}}, {"$set": {"deleted_at": datetime.utcnow()}})
    return {"count": update_deleted_at.modified_count}


@app.patch("/delete-subtask", tags=["Task Deletion"])
def delete_subtask(subtask_id: int):
    # retriving task_id from subtask_id
    subtasks = (test_subtask.find_one(
        {"id": subtask_id, "deleted_at": {"$eq": None}}))
    update_task_status(subtasks.get("task_id"))

    update_deleted_at = test_subtask.update_one(
        {"id": subtask_id, "deleted_at": {"$eq": None}}, {"$set": {"deleted_at": datetime.utcnow()}})
    # update_task_status(test_subtask.find(
    #     {"id": subtask_id, "deleted_at": {"$eq": None}}).get("task_id"))

    return {"count": update_deleted_at.modified_count}


@app.get("/all-user-subtask", tags=["Task Retrieve"])
def all_user_subtask(task_id: int):
    subtasks = []
    all_subtasks = list(test_subtask.find(
        {"task_id": task_id, "deleted_at": {"$eq": None}}))
    for subtask in all_subtasks:
        subtask["_id"] = str(subtask.get("_id"))
        subtasks.append(subtask)
    return {"subtasks": subtasks}


@app.get("/all-user-task", tags=["Task Retrieve"])
def all_user_task(priority: int, due_date: datetime, start_page: int, end_page: int):
    tasks = []
    all_tasks = list(test_task.find(
        {"due_date": due_date, "priority": priority, "deleted_at": {"$eq": None}}).skip(start_page).limit(end_page))
    for task in all_tasks:
        task["_id"] = str(task.get("_id"))
        tasks.append(task)
    return {"tasks": tasks}
