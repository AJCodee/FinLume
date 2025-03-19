from utils import hash_password
from models import User
from sqlalchemy.orm import Session
from database import get_db
from typing import List

class UserCrud:
    """ This class will contain the CRUD operations for the User model. """
    
    @staticmethod
    def create_user(db: Session, user: User) -> User:
        """ Creates a new user in the database. """
        user.hashed_password = hash_password(user.hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    