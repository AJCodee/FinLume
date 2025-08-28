from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import Optional, Annotated
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """ Hashes a password using the bcrypt algorithm. """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verifies a password against a hashed password. """
    return pwd_context.verify(plain_password, hashed_password)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="users/token") # May have to change this to something like tokenurl = "/api/v1/login"

# Define the token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Function to create an access token    
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, Settings.SECRET_KEY, algorithm= Settings.ALGORITHM)

# Function to get the current user from the token
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        paylaod = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        username: str = paylaod.get("sub")
        user_id: int = paylaod.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
       