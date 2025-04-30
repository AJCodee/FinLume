# Routes for Bills.
from fastapi import APIRouter, status
from app.crud.bills_crud import BillCRUD
from app.schemas.bills_schemas import BillCreate, BillUpdate
from app.database import db_dependency

router = APIRouter(tags=["Bills"], prefix="/Bills")

# Calling the BillCrud to use within the Endpoints.
bill_manager = BillCRUD()

# Creating a new Bill to add to the database.
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_bill(bill_data: BillCreate, db: db_dependency):
    return bill_manager.create_new_bill(bill_data=bill_data, db=db)