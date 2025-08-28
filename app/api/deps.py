from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user # wherever you implement it

DbDep = Annotated[Session, Depends(get_db)]
UserDep = Annotated[dict, Depends(get_current_user)]