from fastapi import FastAPI


app = FastAPI()

# Testing that the server works.
@app.get("/")
async def Root():
    return {"message": "Welcome to FinLume"}
