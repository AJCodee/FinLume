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

@router.get("/get-all", status_code=status.HTTP_200_OK)
async def get_all_bills(db: db_dependency):
    return bill_manager.get_all_bills(db=db)

@router.get("/users-bills", status_code=status.HTTP_200_OK)
async def get_bill_by_id(user_id : int, db: db_dependency):
    return bill_manager.get_bill_by_id(user_id=user_id, db=db)

@router.put("/update-bill/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_bill(bill_id: int, bill_data: BillUpdate, db: db_dependency):
    return bill_manager.update_bill(bill_id=bill_id, bill_data=bill_data, db=db)