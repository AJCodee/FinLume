# Will be used for handling user authentication and authorization.
# Create a new user, login, hash passwords and verify them.

from app.utils import hash_password, verify_password
from app.models import User
from app.schemas.user_schemas import UserCreate 
from app.database import db_dependency

class AuthCrud:
    """ This class will handle authentication related CRUD operations. """

    def create_new_user(self, user: UserCreate, db: db_dependency) -> User:
        """ This method will create a new user in the database. 

        Args: 
            user (UserCreate): Contains the user data.

        Returns:
            User: The created User instance.
        """
        self._validate_created_user(user)
        
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            is_active=user.is_active
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    def _validate_created_user(self, user_data: UserCreate):
        """ This method will validate the user data before creating a new user."""
        if not user_data.first_name:
            raise ValueError("First name is required")
        if not user_data.last_name:
            raise ValueError("Last name is required")
        
    def authenticate_user(self, username: str, password: str, db: db_dependency) -> User:
        """ This method will authenticate a user by their username and password. 
        
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            
        Returns:
            User: The authenticated user instance.
            
        Raises:
            ValueError: If the credentials are invalid.
        """
        
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        return user