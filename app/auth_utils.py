from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import Optional, Annotated
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()
# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY") # Secret key for JWT encoding and decoding (Add to .env file)
ALGORITHM = os.getenv("ALGORITHM")
ACCEES_TOKEN_EXPIRE_MINUTES = 30 # Expiration time for access token in minutes

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# Define the token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Function to create an access token    
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    data = {
        "sub": username,
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Function to get the current user from the token
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        paylaod = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = paylaod.get("sub")
        user_id: int = paylaod.get("user_id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
       