# Routes for Bills.
from fastapi import APIRouter, status, HTTPException
from app.crud.bills_crud import BillCRUD
from app.schemas.bills_schemas import BillCreate, BillUpdate, BillResponse
from app.database import db_dependency, user_dependency

router = APIRouter(tags=["Bills"], prefix="/Bills")

# Calling the BillCrud to use within the Endpoints.
bill_manager = BillCRUD()

# Creating a new Bill to add to the database.
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_bill(bill_data: BillCreate, user: user_dependency, db: db_dependency):
    return bill_manager.create_new_bill(bill_data=bill_data, db=db)

# To return all the bills.
@router.get("/get-all", status_code=status.HTTP_200_OK)
async def get_all_bills(user: user_dependency, db: db_dependency):
    bills = bill_manager.get_all_bills(db=db)
    if not bills:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bills found")
    return bills

# Return bills by ID.
@router.get("/bill-by-id/{bill_id}", status_code=status.HTTP_200_OK)
async def get_bill_by_id(bill_id : int, user: user_dependency, db: db_dependency):
    bill = bill_manager.get_bill_by_id(bill_id=bill_id, db=db)
    if not bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")
    return bill

# Return all bills for certain user.
@router.get("/user-bills/{user_id}", status_code=status.HTTP_200_OK)
async def get_bill_per_user(user_id: int, user: user_dependency, db: db_dependency):
    user_bills = bill_manager.get_bill_per_user(user_id=user_id, db=db)
    if not user_bills:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bills found for this user")
    return user_bills

# Updates a bill in the database.
@router.put("/update-bill/{bill_id}", response_model= BillResponse, status_code=status.HTTP_200_OK)
async def update_bill(bill_id: int, bill_data: BillUpdate, user: user_dependency, db: db_dependency):
    try:
        updated_bill = bill_manager.update_bill(bill_id=bill_id, bill_data=bill_data, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found") from e

    return updated_bill

# Deletes a bill in the database.
@router.delete("/delete-bill/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bill(bill_id: int, user: user_dependency, db: db_dependency):
    success = bill_manager.delete_bill(bill_id=bill_id, db=db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")
    return success