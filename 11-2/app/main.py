from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from itertools import count
from threading import Lock
from typing import Dict, List

app = FastAPI(
    title="Async Test API",
    description="API для асинхронного тестирования с Faker",
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
            detail="User not found"
        )
    return {"id": user_id, **db[user_id]}


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if db.pop(user_id, None) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/users")
def delete_all_users():
    db.clear()
    return {"message": "All users deleted"}


@app.get("/users")
def get_all_users() -> List[UserOut]:
    return [{"id": uid, **user} for uid, user in db.items()]