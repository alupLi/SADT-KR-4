# Задание 9.1 - Миграции Alembic в FastAPI

## Установка и запуск

1. Создайте виртуальное окружение:
```bash
python -m venv venv

source venv/bin/activate  # или venv\Scripts\activate
```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Примените имиграции:
```bash
alembic upgrade head
```
4. Добавьте тестовые данные:
```bash
python seed.py
```
5. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

## Проверка функциональности

### Проверка структуры таблицы

```bash
python -c "from app.database import SessionLocal; from sqlalchemy import inspect; db=SessionLocal(); inspector=inspect(db.get_bind()); print([c['name'] for c in inspector.get_columns('products')])"
```

Ожидаемый вывод: ['id', 'title', 'price', 'count', 'description']

### Проверка количества записей

```bash
python -c "from app.database import SessionLocal; from app.models import Product; db=SessionLocal(); print(f'Записей: {db.query(Product).count()}')"
```

Ожидаемый вывод: 2

---


# Задание 10.1 — Пользовательская обработка ошибок в FastAPI

## Установка и запуск

```bash
python -m venv venv

source venv/bin/activate  # или venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Проверка функциональности
1. Успешные запросы
```bash
# Получить существующий товар
curl http://localhost:8000/api/items/1

# Валидный товар
curl -X POST "http://localhost:8000/api/items/validate?name=Laptop&price=999"
```
2. Ошибка 404 (CustomExceptionB)
```bash
# Несуществующий товар
curl http://localhost:8000/api/items/999
Ожидаемый ответ:

json
{
  "status_code": 404,
  "error_type": "Not Found",
  "message": "Товар с id=999 не найден",
  "timestamp": "2026-04-30T13:00:00",
  "path": "/api/items/999"
}
```
3. Ошибка 400 (CustomExceptionA)
```bash
# Цена меньше или равна 0
curl -X POST "http://localhost:8000/api/items/validate?name=Mouse&price=0"

# Название слишком короткое
curl -X POST "http://localhost:8000/api/items/validate?name=AB&price=100"
Ожидаемый ответ:

json
{
  "status_code": 400,
  "error_type": "Validation Error",
  "message": "Цена товара должна быть больше 0",
  "timestamp": "2026-04-30T13:00:00",
  "path": "/api/items/validate"
}
```
---



# Задание 10.2 — Валидация данных запроса в FastAPI

## Установка и запуск

```bash
python -m venv venv

source venv/bin/activate  # или venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Тестирование API

1. Успешная регистрация
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ivanpetrov",
    "age": 25,
    "email": "ivan@example.com",
    "password": "securepass123"
  }'
```
2. Ошибки валидации

Неверный возраст (<= 18)
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "age": 17,
    "email": "test@example.com",
    "password": "pass12345"
  }'
``` 

Неверный email
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "age": 25,
    "email": "not-an-email",
    "password": "pass12345"
  }'
``` 

Слишком короткий пароль (< 8 символов)
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "age": 25,
    "email": "test@example.com",
    "password": "short"
  }'
``` 

Слишком короткий username (< 3 символов)
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ab",
    "age": 25,
    "email": "test@example.com",
    "password": "longpassword123"
  }'
``` 

---



# Задание 11.1 — Модульные тесты для FastAPI

## Установка

```bash
python -m venv venv

source venv/bin/activate  # или venv\Scripts\activate

pip install -r requirements.txt
```

## Запуск тестов
```bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск конкретного тестового файла
pytest tests/test_users.py

# Запуск конкретного теста
pytest tests/test_users.py::TestUserAPI::test_create_user_success -v
```

## Запуск приложения
```bash
uvicorn app.main:app --reload
```

## Ожидаемый результат тестов

```
============================= test session starts =============================
collected 11 items

tests/test_users.py ...........                                          [100%]
tests/test_integration.py ..                                              [100%]

============================= 13 passed in 0.52s ==============================
```

## Проверка покрытия

```bash
# Установка pytest-cov
pip install pytest-cov

# Запуск с покрытием
pytest --cov=app --cov-report=term
```

---



# Задание 11.2 — Асинхронные тесты с Faker

## Установка

```bash
python -m venv venv

source venv/bin/activate  # или venv\Scripts\activate

pip install -r requirements.txt
```

## Запуск тестов

```bash
# Запуск всех асинхронных тестов
pytest -v

# Запуск конкретного файла
pytest tests/test_users_async.py -v

# Запуск с выводом print (для отладки)
pytest -v -s
```

## Ожидаемый результат

```
============================= test session starts =============================
platform win32 -- Python 3.12.0, pytest-8.3.4, pluggy-1.5.0
rootdir: .../11-2_async_tests
configfile: pytest.ini
plugins: asyncio-0.24.0
asyncio: mode=auto

collected 13 items

tests/test_users_async.py .........                                      [ 69%]
tests/test_faker_edge_cases.py ....                                      [100%]

============================= 13 passed in 0.85s ==============================
```

## Запуск приложения

```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /users` - создание пользователя
- `GET /users/{id}` - получение пользователя
- `DELETE /users/{id}` - удаление пользователя
- `DELETE /users` - очистка всех пользователей (для тестов)