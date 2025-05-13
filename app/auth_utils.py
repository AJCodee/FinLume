from datetime import datetime, timedelta
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

# code for generating JWT tokens for user.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class Token(BaseModel):
    access_token: str
    token_type: str
    
# This function creates a signed JWT token with an expiration time.
# The token contains the user ID and other claims.
# The token is signed using the secret key and algorithm specified in the environment variables.
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt