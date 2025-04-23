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