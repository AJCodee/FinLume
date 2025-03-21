from fastapi import FastAPI
from app.routers.user_routes import router as user_router


app = FastAPI()

# Testing that the server works.
@app.get("/")
async def Root():
    return {"message": "Welcome to FinLume"}


app.include_router(user_router)