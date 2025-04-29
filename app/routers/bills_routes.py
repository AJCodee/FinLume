# Routes for Bills.
from fastapi import APIRouter, status
from app.crud.bills_crud import BillCRUD
from app.schemas.bills_schemas import BillCreate, BillUpdate
from app.database import db_dependency