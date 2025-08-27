# Endpoints for Subscriptions.

from fastapi import APIRouter, status, HTTPException
from app.crud.sub_crud import SubscriptionCrud
from app.schemas.sub_schemas import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from app.database import db_dependency, user_dependency

router = APIRouter(tags=["Subscription"], prefix='/Subscription')

# Calling the SubscriptionCrud class to use in the endpoint. 
sub_manager = SubscriptionCrud()

# Creating a new Subscription
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_subscriptions(subscriptions: SubscriptionCreate, user: user_dependency, db: db_dependency):
    return sub_manager.create_new_subscriptions(sub=subscriptions, db=db)

# Returns all subscriptions in database
@router.get("/get-all", status_code=status.HTTP_200_OK)
async def get_all_subscriptions(user: user_dependency, db: db_dependency):
    subscriptions = sub_manager.get_all_subscriptions(db=db)
    if not subscriptions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscriptions found")
    return subscriptions

# Returns all the subscriptions for a select user
@router.get("/user-subscriptions/{user_id}", status_code=status.HTTP_200_OK)
async def subscriptions_per_user(user_id: int, user: user_dependency, db: db_dependency):
    user_subscriptions = sub_manager.subscriptions_per_user(user_id=user_id, db=db)
    if not user_subscriptions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscriptions found for this user")
    return user_subscriptions

# Return a subscription by ID
@router.get("/get-by-id/{sub_id}", status_code=status.HTTP_200_OK)
async def get_subscription_by_id(sub_id: int, user: user_dependency, db: db_dependency):
    subs = sub_manager.get_subscription_by_id(sub_id=sub_id, db=db)
    if not subs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return subs

# Update a subscription
@router.put("/update/{sub_id}", response_model= SubscriptionResponse, status_code=status.HTTP_200_OK)
async def update_subscription(sub_id: int, sub: SubscriptionUpdate, user: user_dependency, db: db_dependency):
    try:
        updated_subscription = sub_manager.update_subscription(sub_id=sub_id, sub=sub, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return updated_subscription

# Delete a subscription
@router.delete("/delete/{sub_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(sub_id: int, user: user_dependency, db: db_dependency):
    success = sub_manager.delete_subscription(sub_id=sub_id, db=db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return success