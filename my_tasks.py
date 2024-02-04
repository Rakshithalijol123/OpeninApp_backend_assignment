# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from pymongo import MongoClient
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

DATABASE_URL = "mongodb://localhost:27017"
client = MongoClient(DATABASE_URL)
db = client["your_database_name"]
test_user = db["Test_user"]
test_task = db["Test_task"]
test_subtask = db["Test_subtask"]


class UserDBModel(BaseModel):
    id: int
    phone_number: int
    priority: int


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


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


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


def update_priority(task_id: int, due_date: datetime):
    updated_task_status = test_task.update_one(
        {"id": task_id, "deleted_at": {"$eq": None}}, {"$set": {"updated_at": datetime.utcnow(), "priority": get_priority(due_date)}})
    return {"Count": updated_task_status.modified_count}


def get_tasks():
    # Fetch tasks from MongoDB
    tasks = [TaskDBModel(**task) for task in test_task.find()]
    return tasks

# Function to fetch users


def get_users():

    # Fetch users from MongoDB
    users = [UserDBModel(**user) for user in test_user.find()]
    return users


def make_twilio_call(to_phone_number: str):
    # Initialize Twilio client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Twilio call logic
    try:
        call = client.calls.create(
            to=to_phone_number,
            from_=TWILIO_PHONE_NUMBER,
            # Replace with your TwiML URL or TwiML content
            url="http://demo.twilio.com/docs/voice.xml"
        )
        print(f"Call initiated to {to_phone_number}, Call SID: {call.sid}")
        return True  # Call successfully initiated
    except Exception as e:
        print(f"Failed to initiate call to {to_phone_number}: {str(e)}")
        return False  # Call initiation failed


def update_user_status(user: UserDBModel):
    try:
        # Replace with your MongoDB connection string

        # Update the user's status in the collection
        test_user.update_one(
            {"id": user.id},
            {"$set": {"called": user.called}}
        )

        print(f"User status updated in MongoDB for user with ID: {user.id}")
    except Exception as e:
        print(f"Failed to update user status in MongoDB: {str(e)}")


def get_users_to_call(tasks: List[TaskDBModel], users: List[UserDBModel]) -> List[str]:
    # Get current datetime
    current_datetime = datetime.utcnow()

    # Filter tasks that have passed their due dates and have status "TODO" or "IN_PROGRESS"
    overdue_tasks = [task for task in tasks if task.due_date <
                     current_datetime and task.status in ["TODO", "IN_PROGRESS"]]

    # Sort users based on priority
    sorted_users = sorted(users, key=lambda user: user.priority)

    previous_priority = None  # Keep track of the previous user's priority
    users_to_call = []  # List to store phone numbers of users to call

    for task in overdue_tasks:
        # Find the corresponding user for the task
        user = next((u for u in sorted_users if u.id == task.user_id), None)

        if user and user.priority != previous_priority and not user.called:
            # Attempt to make Twilio call
            if make_twilio_call(user.phone_number):
                # Update the user's status to indicate a successful call attempt
                user.called = True

                # Update the user's status in the MongoDB user collection
                # Assuming you have a function to update the user status, adjust accordingly
                update_user_status(user)

                # Add the user's phone number to the list
                users_to_call.append(user.phone_number)

                # Update the previous_priority for the next iteration
                previous_priority = user.priority

    return users_to_call
