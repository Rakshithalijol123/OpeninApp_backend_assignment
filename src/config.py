import os
import json
import secrets
from typing import Dict
# --- About The App ---
APP_NAME = os.getenv("APP_NAME", "TASK MANAGER")
APP_DESCRIPTION = "http server for task manager"


APP_HOST = "localhost"
APP_PORT = 8000


# Number of concurrent processes
APP_WORKER = int(os.getenv("APP_WORKER", 1))

# Endpoint to Swagger UI
SWAGGER_ENDPOINT = os.getenv("SWAGGER_ENDPOINT", "/docs")

# --- JWT token details ---
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# --- SERVICE ---
USERNAME = "547353cb38f248482ee2d404ab38ad5a16bd073bd023efe0fcad693e6936eb4c"
PASSWORD = "d8ae0c4a2cac77d554136dae65a4e36cb63e990dbd5b9bfc22ca2b7d0dc50a7d"
