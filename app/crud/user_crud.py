from app.models import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.database import db_dependency
from app.crud.bills_crud import BillCRUD
from app.crud.sub_crud import SubscriptionCrud

bill_manager = BillCRUD()
sub_manager = SubscriptionCrud()

class UserCrud:
    """ This class will contain the CRUD operations for the User model. """
    
    def update_user(self, user_id: int, user_data: UserUpdate, db: db_dependency) -> User:
        """ This method will update a user in the database. 
        
        Args:
            user_id (int): The ID of the user to Update.
            user_data (UserCreate): The updated data.
            
        Returns:
            User: The updated user instance.
            
        Raises:
            ValueError: If the User does not exist or the data is invalid.
        """
        
        exsisting_user = self.get_user_by_id(user_id, db)
        if not exsisting_user:
            raise ValueError("User does not exist")
        
        self._apply_updates(exsisting_user, user_data)
        
        try:
            db.commit()
            return exsisting_user
        except Exception as e:
            db.rollback()
            raise ValueError("Failed to update user") from e
    
    def get_all_users(self, db: db_dependency):
        """ This Method will return all users in the database """
        return db.query(User).all()
        
    def get_user_by_id(self, user_id: int, db: db_dependency):
        """ This method will return a user by their id """
        return db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str, db: db_dependency):
        """ This method will return a user by their username """
        return db.query(User).filter(User.username == username).first()
    
    def get_user_payments(self, user_id: int, db: db_dependency):
        """ This method will be for returning all the bills and Subscriptions for a user. """
        bills = bill_manager.get_bill_per_user(user_id=user_id, db=db)
        subscription = sub_manager.subscriptions_per_user(user_id=user_id, db=db)
        return bills, subscription 
    
    def _apply_updates(self, exsisting_user: User, user_update: UserUpdate):
        """ This method will apply the updates to the existing user """
        if user_update.first_name is not None:
            exsisting_user.first_name = user_update.first_name
        if user_update.last_name is not None:
            exsisting_user.last_name = user_update.last_name
        if user_update.username is not None:
            exsisting_user.username = user_update.username
        if user_update.email is not None:
            exsisting_user.email = user_update.email
        if user_update.is_active is not None:
            exsisting_user.is_active = user_update.is_active
    
    def delete_user(self, user_id: int, db: db_dependency):
        """ This method will delete a user from the database """
        exsisting_user = self.get_user_by_id(user_id, db)
        if not exsisting_user:
            raise ValueError("User does not exist")
        try:
            db.delete(exsisting_user)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValueError("Failed to delete user") from e
            