from fastapi import FastAPI
from app.routers.user_routes import router as user_router
from app.routers.sub_routes import router as sub_router
from app.routers.bills_routes import router as bill_router
from app.database import engine, Base

# Initiates FastAPI.
app = FastAPI()

# Creates the tables in the database.
Base.metadata.create_all(bind=engine)

# Testing that the server works.
@app.get("/")
async def Root():
    return {"message": "Welcome to FinLume"}

# Included router to activate it.
app.include_router(user_router)
app.include_router(sub_router)
app.include_router(bill_router)