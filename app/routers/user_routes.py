from fastapi import APIRouter, Depends
from app.models import User
from app.schemas.user_schemas import UserBase, UserUpdate, UserResponse

router = APIRouter(tags=["Users"], prefix="/users")

