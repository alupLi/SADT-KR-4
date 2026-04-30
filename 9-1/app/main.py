from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Product
from pydantic import BaseModel

app = FastAPI()

Base.metadata.create_all(bind=engine)

class ProductCreate(BaseModel):
    title: str
    price: float
    count: int

class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    count: int

@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product