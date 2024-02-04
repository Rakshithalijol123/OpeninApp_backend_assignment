import jwt
import json
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from jwt import DecodeError
from fastapi.security import OAuth2PasswordBearer
from src.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, USERNAME, PASSWORD
)
from typing import Dict
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth/token")


def authenticate_user(username, password):
    if username == USERNAME and password == PASSWORD:
        access_token_expires = datetime.utcnow(
        ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {'sub': username, "exp": access_token_expires}
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return access_token
    return None


def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return username
    except DecodeError:
        # Handle token decoding error
        raise HTTPException(
            status_code=401,
            detail={
                "title": "Authorization Header Missing",
                "details": "Authorization token not found in request header",
                "status": 401,
            },
        )
