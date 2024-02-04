from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
import pymongo
import jwt

app = FastAPI()

# MongoDB connection details
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["OpeninApp_Assignment"]
users_collection = db["users"]

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    password: str
    phone_no: str
    priority: int

# Function to create a JWT token


def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to decode JWT token


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token", headers={
                            "WWW-Authenticate": "Bearer"})

# Function to get current user from token


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials = decode_jwt_token(token)
    return credentials

# Endpoint to create a new user and generate a JWT token


@app.post("/register", response_model=dict)
async def register_user(user: User):
    # Hash the password in a real-world scenario
    hashed_password = user.password

    # Save user details to MongoDB
    user_data = {
        "username": user.username,
        "password": hashed_password,
        "phone_no": user.phone_no,
        "priority": user.priority,
    }
    user_id = users_collection.insert_one(user_data).inserted_id

    # Create JWT token
    access_token_expires = timedelta(minutes=15)
    access_token = create_jwt_token(
        data={"sub": str(user_id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Example protected route that requires a valid JWT token


@app.get("/protected", response_model=dict)
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user_id": current_user["sub"]}
