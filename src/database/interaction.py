from .connection import (
    connect,
    create_database
)

client = connect("mongodb://localhost:27017")
db = create_database(client=client, db_name="TASKS")


# --- Create your collections here ---
users_collection = db["users"]
tasks_collection = db["tasks"]
subtasks_collection = db["subtasks"]

# Write functions which interact with database


# def create_user(userData: dict) -> str:
#     user = User.insert_one(userData)
#     return str(user.inserted_id)
