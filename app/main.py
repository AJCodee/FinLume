from fastapi import FastAPI
from app.api.user_routes import router as user_router
from app.api.auth_routes import router as auth_router
from app.db.session import engine
from app.db.models import Base

# Initiates FastAPI.
app = FastAPI()

# Creates the tables in the database.
Base.metadata.create_all(bind=engine)

# Testing that the server works.
@app.get("/")
async def Root():
    return {"message": "Welcome to FinLume"}

# Included router to activate it.
app.include_router(auth_router)
app.include_router(user_router)
