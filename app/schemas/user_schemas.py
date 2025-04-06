# This is the Schema for the User model.

from pydantic import BaseModel, StringConstraints, EmailStr
from typing import Optional, Annotated

class UserBase(BaseModel):
    """ Base Model for a user, containing the common attributes. """
    first_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    last_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    username: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    email: EmailStr
    is_active: Optional[bool] = True
    
class UserCreate(UserBase):
    """ Inherits from UserBase and add password here as it is sensitive information """
    password: str # A required feild in the Usercreate class.
    
class UserUpdate(BaseModel):
    """ Model for updating user information, allowing for partial updates. """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """ Model for user responses, Includes the user's ID. """
    id: int
    
    class Config:
        from_attributes = True
        