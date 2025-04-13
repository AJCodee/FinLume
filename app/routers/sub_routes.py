# Endpoints for Subscriptions.

from fastapi import APIRouter, status
from app.crud.sub_crud import SubscriptionCrud
from app.schemas.sub_schemas import SubscriptionCreate, SubscriptionUpdate
from app.database import db_dependency

router = APIRouter(tags=["subscription"], prefix='/subscription')

sub_manager = SubscriptionCrud()

# Creating a new Subscription
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_subscriptions(subscriptions: SubscriptionCreate, db: db_dependency):
    return sub_manager.create_new_subscriptions(sub=subscriptions, db=db)

# Returns all subscriptions in database
@router.get("/get-all", status_code=status.HTTP_200_OK)
async def get_all_subscriptions(db: db_dependency):
    return sub_manager.get_all_subscriptions(db=db)

# Returns all the subscriptions for a select user
@router.get("/user-subscriptions", status_code=status.HTTP_200_OK)
async def subscriptions_per_user(user_id: int, db: db_dependency):
    return sub_manager.subscriptions_per_user(user_id=user_id, db=db)
