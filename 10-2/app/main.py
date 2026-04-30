from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.models import User
from app.error_handlers import validation_exception_handler, generic_validation_error_handler

app = FastAPI(
    title="User Registration API",
    description="API с валидацией данных и обработкой ошибок",
    version="1.0.0"
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, generic_validation_error_handler)

users_db = {}


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Пользователь с именем '{user.username}' уже существует"
        )
    
    for existing_user in users_db.values():
        if existing_user['email'] == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Пользователь с email '{user.email}' уже существует"
            )
    
    user_id = len(users_db) + 1
    users_db[user.username] = {
        "id": user_id,
        "username": user.username,
        "age": user.age,
        "email": user.email,
        "phone": user.phone
    }
    
    return {
        "message": "Пользователь успешно зарегистрирован",
        "user_id": user_id,
        "user": users_db[user.username]
    }


@app.get("/users/{username}")
async def get_user(username: str):
    if username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь '{username}' не найден"
        )
    
    return users_db[username]


@app.get("/users")
async def get_all_users():
    return list(users_db.values())


@app.get("/")
async def root():
    return {
        "message": "API регистрации пользователей",
        "endpoints": [
            "POST /register - регистрация пользователя",
            "GET /users/{username} - получить пользователя",
            "GET /users - список всех пользователей"
        ]
    }