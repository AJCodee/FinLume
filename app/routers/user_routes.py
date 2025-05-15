from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.crud.user_crud import UserCrud 
from app.auth_utils import create_access_token
from app.database import db_dependency
from typing import List

router = APIRouter(tags=["Users"], prefix="/users")

user_manager = UserCrud()

# Creating a new user.
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: db_dependency):
    return user_manager.create_new_user(user=user, db=db)

@router.post("/token", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordBearer = Depends()):
    user = user_manager.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "user": user}

# Returning all users    
@router.get("/return-users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    users = user_manager.get_all_users(db=db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users

# Returning a user by ID
@router.get("/user-by-id/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: db_dependency):
    user = user_manager.get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Endpoint for returning all the bills and subscription for user.
@router.get("/all-payments/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_payments(user_id: int, db: db_dependency):
    user_data = user_manager.get_user_payments(user_id=user_id, db=db)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_data

# Updating a user in the database
# Using Patch for partial updates. As if you use PUT to change one feild causes feilds you dont change to reset to default.
@router.put("/update-user/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_data: UserUpdate, db: db_dependency):
    updated_user = user_manager.update_user(user_id=user_id, user_data=user_data, db=db)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return update_user

# Deleting a user from the database
@router.delete("/delete-user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: db_dependency):
    success = user_manager.delete_user(user_id=user_id, db=db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return success
