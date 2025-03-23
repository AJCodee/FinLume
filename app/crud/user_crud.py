from app.utils import hash_password
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user_schemas import UserBase, UserCreate, UserResponse, UserUpdate
from app.database import db_dependency
from typing import List

class UserCrud:
    """ This class will contain the CRUD operations for the User model. """
    
    @staticmethod
    def create_new_user(user: UserCreate, db: db_dependency):
        """ This method will create a new user in the database. """
        new_user = User(
            first_name = user.first_name,
            last_name = user.last_name,
            username = user.username,
            email = user.email,
            hashed_password = hash_password(user.password),
            is_active = user.is_active
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
    