from fastapi import FastAPI
from app.routers.user_routes import router as user_router
from app.database import engine, Base


app = FastAPI()

# Creates the tables in the database.
Base.metadata.create_all(bind=engine)

# Testing that the server works.
@app.get("/")
async def Root():
    return {"message": "Welcome to FinLume"}


app.include_router(user_router)