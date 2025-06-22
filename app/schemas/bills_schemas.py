# This is the Schemasfor the Bills model.

from pydantic import BaseModel, StringConstraints
from datetime import date
from typing import Optional, Annotated

class BillBase(BaseModel):
    """ Schema for creating a new bill """
    title: Annotated[str, StringConstraints(min_length=3, max_length=20)]
    amount: float
    due_date: date
    
class BillCreate(BillBase):
    """Model for creating a new Bill"""
    user_id: int # Used to link a Bill to a user.
    
class BillUpdate(BillBase):
    """Model for updating an existing Bill"""
    
    title: Optional[str] = None
    amount: Optional[float] = None
    due_date: Optional[date] = None
    
class BillResponse(BillBase):
    """Model for the response of a Bill includes Bill ID"""
    
    id: int
    user_id: int # Used to return the ID of the User associated with this Bill.
    
    class ConfigDict:
        from_attributes = True