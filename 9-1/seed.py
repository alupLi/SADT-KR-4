from app.database import SessionLocal
from app.models import Product

db = SessionLocal()

p1 = Product(title="Laptop", price=999.99, count=10)
p2 = Product(title="Mouse", price=19.99, count=50)

db.add_all([p1, p2])
db.commit()
db.close()

print("Добавлено 2 товара")