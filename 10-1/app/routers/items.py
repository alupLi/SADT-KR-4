from fastapi import APIRouter, Request
from app.exceptions import CustomExceptionA, CustomExceptionB

router = APIRouter(prefix="/api", tags=["items"])

items_db = {
    1: {"id": 1, "name": "Laptop", "price": 999},
    2: {"id": 2, "name": "Mouse", "price": 25},
}


@router.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise CustomExceptionB(f"Товар с id={item_id} не найден")
    return {"item": items_db[item_id]}


@router.post("/items/validate")
def validate_item(name: str, price: float):
    if price <= 0:
        raise CustomExceptionA("Цена товара должна быть больше 0")
    
    if len(name) < 3:
        raise CustomExceptionA("Название товара должно содержать минимум 3 символа")
    
    return {"message": "Товар валиден", "name": name, "price": price}