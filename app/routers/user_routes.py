from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse
from app.crud.user_crud import UserCrud 
from app.database import db_dependency
from typing import List

router = APIRouter(tags=["Users"], prefix="/users")

user_manager = UserCrud()

# Creating a new user.
@router.post("/usercreate", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: db_dependency):
    return user_manager.create_new_user(user=user, db=db)

# Returning all users    
@router.get("/return_users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    return user_manager.get_all_users(db=db)

# Returning a user by ID
@router.get("/user_by_id/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: db_dependency):
    return user_manager.get_user_by_id(user_id=user_id, db=db)

# Updating a user in the database
# Using Patch for partial updates. As if you use PUT to change one feild causes feilds you dont change to reset to default.
@router.put("/update_user/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_data: UserUpdate, db: db_dependency):
    return user_manager.update_user(user_id=user_id, user_data=user_data, db=db)

# Deleting a user from the database