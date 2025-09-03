from __future__ import annotations

from pydantic import BaseModel, StringConstraints
from typing import Annotated, Optional

class TransactionBase(BaseModel):
    """ Base Model for Transaction """
    
    merchant: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    amount: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    posted_at: Annotated[]
    note: 
