from app.database import db_dependency
from app.models import Bill
from app.schemas.bills_schemas import BillCreate, BillUpdate

class BillCRUD:
    """ This class will contain the CRUD Functions for the bill model. """
    
    def create_new_bill(self, bill_data: BillCreate, db: db_dependency) -> Bill:
        """ Create a new bill in the database
        
        Args:
            bill_data (BillCreate): The data for the new bill to be created
            db (Session): The database session to use for the operation
            
        Response:
            Bill: The created bill object
        """
        new_bill = Bill(
            title = bill_data.title,
            amount = bill_data.amount,
            due_date = bill_data.due_date,
            user_id = bill_data.user_id # Foregin Key
        )
        
        db.add(new_bill)
        db.commit()
        db.refresh(new_bill)
        
        return new_bill
    
    def update_bill(self, bill_id: int, bill_data: BillUpdate, db: db_dependency) -> Bill:
        """ Model for updating a Bill in the database 
        
        Args:
            bill_id (int) ID of the exsisting bill in database
            bill_data (BillUpdate) The updated data 
            
        Response:
            Bill: The updated Bill data
            
        Raises:
            ValueError: Raises error if the exsisting Bill doesnt exsist in database
        """
        
        exsisting_bill = get_bill_by_id(bill_id, db)
        if not exsisting_bill:
            raise ValueError("Bill does not exsist.")
        
        self._apply_updates(exsisting_bill, bill_data) # Create the _apply_updates function below.
        
        try:
            db.commit()
            return exsisting_bill
        except Exception as e:
            db.rollback()
            raise Exception("Failed to update Bill") from e 
            