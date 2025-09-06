from __future__ import annotations

from pydantic import BaseModel, StringConstraints
from typing import Annotated, Optional

class CategoryBase(BaseModel):
    """ Base model for category """
    name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    
class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    """ Model for updating a Category information """
    name: Optional[Annotated[str, StringConstraints(min_length=2, max_length=50)]] = None
    
class CategoryResponse(BaseModel):
    """ Model for Category responses """
    
    id: int
    name: str
    
    model_config = {"from_attributes": True}
    