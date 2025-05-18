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

# LIST OF THINGS TO DO FOR JWT AUTH: (Maybe create an Auth.py file)
# 1. Create a class BaseModel for the new user (UserCreate)
# 2. Create a class for Token (access_token / token_type)
# 3. Create a Post Endpoint for Creating a new user (UserCreate) Check mine in user_schemas.py
# 4. Create a post for login_for_access_token (UserLogin)
# 5. Create a function for authenticate_user (Check mine in user_schemas.py)
# 6. Create a function for create_access_token (Check mine in user_schemas.py)
# 7. Create a function for get_current_user (Check mine in user_schemas.py) create a dependency.