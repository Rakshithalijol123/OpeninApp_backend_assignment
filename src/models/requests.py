from pydantic import BaseModel, Field
from datetime import datetime


# class UserDataModel(BaseModel):
#     username: str = Field(
#         description="The login username of the user", default="")
#     password: str = Field(
#         description="The login password of the user", default="")


class User(BaseModel):
    id: int = Field(
        description="Unique Identifier for user", default=-1)
    phone_number: int = Field(
        description="Phone number of a user", default=0)
    priority: int = Field(
        description="Priority for the task", default=-1)


class SubTaskModel(BaseModel):
    id: int = Field(
        description="Unique Identifier for user", default=-1)
    task_id: int = Field(
        description="Unique Identifier for tasks", default=0)
    status: int = Field(
        description="Work status of a task", default=-1)
    created_at: datetime = Field(
        description="Task Created date", default=0)
    updated_at: datetime = Field(
        description="Task Updated date", default=0)
    deleted_at: datetime = Field(
        description="Task Deleted date", default=0)


class PriorityTaskModel(BaseModel):
    priority: int = Field(
        description="Priority for the task", default=-1)


class StatusTaskModel(BaseModel):
    progress: str = Field(
        description="Progress for the task", default="")


class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
