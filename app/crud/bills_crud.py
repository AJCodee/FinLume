from app.database import db_dependency
from app.models import Bills
from app.schemas.bills_schemas import BillCreate, BillUpdate

class BillCRUD:
    """ This class will contain the CRUD Functions for the bill model. """
    
    def create_new_bill(self, bill_data: BillCreate, db: db_dependency) -> Bills:
        """ Create a new bill in the database
        
        Args:
            bill_data (BillCreate): The data for the new bill to be created
            db (Session): The database session to use for the operation
            
        Response:
            Bill: The created bill object
            
        Raises:
            ValueError if bill_data can not be validated.
        """
        self._validate_bill(bill_data)
        
        new_bill = Bills(
            title = bill_data.title,
            amount = bill_data.amount,
            due_date = bill_data.due_date,
            user_id = bill_data.user_id # Foregin Key
        )
        
        db.add(new_bill)
        db.commit()
        db.refresh(new_bill)
        
        return new_bill
    
    def update_bill(self, bill_id: int, bill_data: BillUpdate, db: db_dependency) -> Bills:
        """ Model for updating a Bill in the database 
        
        Args:
            bill_id (int) ID of the exsisting bill in database
            bill_data (BillUpdate) The updated data 
            
        Response:
            Bill: The updated Bill data
            
        Raises:
            ValueError: Raises error if the exsisting Bill doesnt exsist in database
        """
        
        exsisting_bill = self.get_bill_by_id(bill_id, db)
        if not exsisting_bill:
            raise ValueError("Bill does not exsist.")
        
        self._apply_updates(exsisting_bill, bill_data) # Create the _apply_updates function below.
        
        try:
            db.commit()
            return exsisting_bill
        except Exception as e:
            db.rollback()
            raise Exception("Failed to update Bill") from e 
        
    def _validate_bill(self, bill_data: BillCreate):
        """ Function for checking is the created Bill is Valid """
        
        if not bill_data.title or len(bill_data.title) == 0:
            raise ValueError("Title is required")
        
        if bill_data.amount <= 0:
            raise ValueError("Amount is required and can not be 0")
        
    def get_all_bills(self, db: db_dependency) -> list[Bills]:
        """ Used to retrieve all Bills in database """
        return db.query(Bills).all()
        
    def get_bill_by_id(self, bill_id: int, db: db_dependency) -> Bills:
        """ Used to retrieve a bill bu ID """
        return db.query(Bills).filter(Bills.id == bill_id).first()
    
    def get_bill_per_user(self, user_id: int, db: db_dependency):
        """ Retrives all the bills for a specific user """
        return db.query(Bills).filter(Bills.user_id == Bills.user_id).all()
    