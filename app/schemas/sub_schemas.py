# This is the Schemas for the Subscription model.

from pydantic import BaseModel, StringConstraints
from datetime import date
from typing import Optional, Annotated

class SubscriptionBase(BaseModel):
    """Base model for Subscription, defines the common attributes"""
    
    service_name: Annotated[str, StringConstraints(min_length=3, max_length=20)]
    monthly_cost: float
    renewal_date: date
    
class SubscriptionCreate(SubscriptionBase):
    """Model for creating a new Subscription"""
    user_id: int # Used to link a Subscription to a User

class SubscriptionUpdate(SubscriptionBase):
    """Model for updating an existing Subscription"""
    
    service_name: Optional[str] = None
    monthly_cost: Optional[float] = None
    renewal_date: Optional[date] = None

class SubscriptionResponse(SubscriptionBase):
    """Model for the response of a Subscription Includes Subscription ID"""
    
    id: int
    user_id: int # Used to return the ID of the User associated with this Subscription
    
    class ConfigDict:
        from_attributes = True