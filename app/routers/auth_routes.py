# Used for authentication routes.
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud.auth_crud import AuthCrud 
from app.schemas.user_schemas import UserCreate, UserResponse
from app.database import db_dependency
from app.auth_utils import Token, create_access_token