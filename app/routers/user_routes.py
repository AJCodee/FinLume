from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse
from app.crud.user_crud import UserCrud 
from app.database import db_dependency
from typing import List

router = APIRouter(tags=["Users"], prefix="/users")

# Creating a new user.
@router.post("/usercreate", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: db_dependency):
    return UserCrud.create_new_user(user, db)

# Returning all users    
@router.get("/return_users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def return_users(db: db_dependency):
    return UserCrud.get_all_users(db)

# Returning a user by ID
@router.get("/user_by_id/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    return UserCrud.get_user_by_id(user_id, db)

# Updating a user in the database
@router.put("/update_user/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserUpdate, db: db_dependency):
    return UserCrud.update_user(user_id, user, db)