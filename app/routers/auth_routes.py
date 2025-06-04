# Used for authentication routes.
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud.auth_crud import AuthCrud 
from app.crud.user_crud import UserCrud
from app.schemas.user_schemas import UserCreate, UserResponse
from app.database import db_dependency
from app.auth_utils import Token, create_access_token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(tags=["Auth"], prefix="/auth")

auth_manager = AuthCrud()
user_manager = UserCrud()

# Endpoint to create a new user
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: db_dependency):
    """Endpoint to register a new user."""
    existing_user = user_manager.get_user_by_username(username=user.username, db=db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    return auth_manager.create_new_user(user=user, db=db)

@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    """ This endpoint will create a new access token for the user. """
    user = auth_manager.authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}
