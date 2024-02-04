# Flow

- Create a virtual environment
- pip install -r requirement.txt

# To run the server

python run.py

# New Updates

- oAuth2 authentication is added
- Get required username and password from config file
- create app based endpoints then add them in main using
  from src.apps.credentials.views import router as credentials_router
  app.include_router(credentials_router, prefix="/credentials",
  dependencies=[Depends(validate_token)])

- src/apps/credentials/views.py
  from fastapi import APIRouter
  from .urls import USER_CREATE_PATH
  import src.database.interaction as db
  from src.models.requests import (
  UserDataModel
  )
  from src.models.responses import (
  UserDataModelResponse
  )
  router = APIRouter()

@router.post(USER_CREATE_PATH)
def create_new_user(userData: UserDataModel) -> UserDataModelResponse:
inserted_id = db.create_user(dict(userData))
return {"status": "OK", "inserted_id": inserted_id}
