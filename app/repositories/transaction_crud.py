# Crud for transactions.

from app.db.models import Transaction
from app.schemas.transaction_schemas import TransactionCreate, TransactionUpdate
from app.api.deps import DbDep

class TransactionCrud:
    """ This class will contain all the CRUD operations for the Transaction model. """
    
    def create_new_transaction(self, transaction_id: int, transaction: TransactionCreate, db: DbDep):
        """ This method will create and return a new transaction. """