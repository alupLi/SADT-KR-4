from pydantic import BaseModel, Field, conint, constr, EmailStr
from typing import Optional


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    
    age: conint(gt=18, lt=120) = Field(..., description="Возраст (должен быть больше 18)")
    
    email: EmailStr = Field(..., description="Email адрес")
    
    password: constr(min_length=8, max_length=16) = Field(..., description="Пароль (8-16 символов)")
    
    phone: Optional[str] = Field(default='Unknown', description="Телефон (опционально)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "ivan123",
                "age": 25,
                "email": "ivan@example.com",
                "password": "securepass",
                "phone": "+79991234567"
            }
        }