from __future__ import annotations

from pydantic import BaseModel, StringConstraints
from typing import Annotated, Optional
from datetime import datetime
from decimal import Decimal

class TransactionBase(BaseModel):
    """ Base Model for Transaction """
    
    merchant: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    amount: Decimal
    posted_at: datetime
    note: Annotated[str, StringConstraints(max_length=500)] = ""

class TransactionCreate(TransactionBase):
    """ Model for creating a Transaction """
    category_id: Optional[int] = None
    
class TransactionUpdate(BaseModel):
    """ Model for updating an exsisting Transaction """
    
    merchant: Optional[Annotated[str, StringConstraints(min_length=2, max_length=50)]] = None
    amount: Optional[Decimal] = None
    posted_at: Optional[datetime] = None
    note: Optional[Annotated[str, StringConstraints(max_length=500)]] = None
    category_id: Optional[int] = None
    
class TransactionResponse(BaseModel):
    """ Model for returning a Transaction from database """
    
    id: int
    user_id: int
    category_id: Optional[int]
    merchant: str
    amount: Decimal
    posted_at: datetime
    note: str
    
    model_config = {"from_attributes": True}
    