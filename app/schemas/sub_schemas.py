# This is the Schemas for the Subscription model.

from pydantic import BaseModel, StringConstraints
from datetime import date
from typing import Optional, Annotated

class SubscriptionBase(BaseModel):
    """Base model for Subscription, defines the common attributes"""
    
    title: Annotated[str, StringConstraints(min_length=3, max_length=20)]
    price: float
    description: Annotated[str, StringConstraints(min_length=5, max_length=50)]
    payment_date: date 
    payment_method: str
    is_active: bool
    
class SubscriptionCreate(SubscriptionBase):
    """Model for creating a new Subscription"""
    pass 

class SubscriptionUpdate(SubscriptionBase):
    """Model for updating an existing Subscription"""
    pass

class SubscriptionResponse(SubscriptionBase):
    """Model for the response of a Subscription"""
    
    class Config:
        from_attributes = True