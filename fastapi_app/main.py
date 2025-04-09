from fastapi import FastAPI
import schemas

app = FastAPI()


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    return {"id": "123","name": "John Doe", "email": "john@example.com"}

@app.get("/users/", response_model=list[schemas.User])
async def read_users():
    return [{"id": "123", "name": "John Doe", "email": "john@example.com"}]
