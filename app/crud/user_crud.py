from app.utils import hash_password
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user_schemas import UserBase, UserCreate, UserResponse, UserUpdate
from app.database import db_dependency
from typing import List

class UserCrud:
    """ This class will contain the CRUD operations for the User model. """
    
    def create_new_user(self, user: UserCreate, db: db_dependency):
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
    
    def get_all_users(self, db: db_dependency):
        """ This Method will return all users in the database """
        return db.query(User).all()
        
        
    def get_user_by_id(self, user_id: int, db: db_dependency):
        """ This method will return a user by their id """
        return db.query(User).filter(User.id == user_id).first()
    

    def update_user(self, user_id: int, user_data: UserUpdate, db: db_dependency):
        """ This method will update a user in the database """
        existing_user = db.query(User).filter(User.id == user_id).first()
        
        if not existing_user:
            raise ValueError("User not found")
        
        # Update the feilds from user_data if they are not None
        user_data_dict = user_data.model_dump(exclude_unset=True)
        
        for key, value in user_data_dict.items():
            if value is not None:
                setattr(existing_user, key, value) # PARTIAL UPDATES NOT WORKING
                
        # Commit the changes to the database
        db.commit()
        db.refresh(existing_user)
        
        return existing_user # Return the updated user