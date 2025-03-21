from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse
from app.crud.user_crud import create_new_user
from database import db_dependency

router = APIRouter(tags=["Users"], prefix="/users")

@router.post("/usercreate", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: db_dependency):
    # Creating a new user.
    return create_new_user(db, user)
    