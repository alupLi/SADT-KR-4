from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List
from itertools import count
from threading import Lock

app = FastAPI(
    title="User Management API",
    description="API для управления пользователями (с тестами)",
    version="1.0.0"
)

db: Dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()

def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)


class UserIn(BaseModel):
    username: str
    age: int


class UserOut(BaseModel):
    id: int
    username: str
    age: int


class UserUpdate(BaseModel):
    username: str | None = None
    age: int | None = None


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn):
    user_id = next_user_id()
    db[user_id] = user.model_dump()
    return {"id": user_id, **db[user_id]}


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return {"id": user_id, **db[user_id]}


@app.get("/users")
def get_all_users() -> List[UserOut]:
    return [{"id": user_id, **user_data} for user_id, user_data in db.items()]


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate):
    if user_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    if user_update.username is not None:
        db[user_id]["username"] = user_update.username
    if user_update.age is not None:
        db[user_id]["age"] = user_update.age
    
    return {"id": user_id, **db[user_id]}


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if db.pop(user_id, None) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return None


@app.delete("/users")
def delete_all_users():
    db.clear()
    return {"message": "All users deleted"}


@app.get("/")
def root():
    return {
        "message": "User Management API",
        "endpoints": [
            "POST /users - create user",
            "GET /users/{id} - get user",
            "GET /users - get all users",
            "PUT /users/{id} - update user",
            "DELETE /users/{id} - delete user",
            "DELETE /users - delete all users (test helper)"
        ]
    }