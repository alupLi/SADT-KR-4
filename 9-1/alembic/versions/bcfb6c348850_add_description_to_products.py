"""add description to products

Revision ID: bcfb6c348850
Revises: 03ce250ac89e
Create Date: 2026-04-30 13:10:02.055256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'bcfb6c348850'
down_revision: Union[str, Sequence[str], None] = '03ce250ac89e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite не поддерживает ALTER COLUMN SET NOT NULL
    # Поэтому делаем так:
    
    # 1. Создаём новую таблицу с нужной структурой
    op.execute('''
        CREATE TABLE products_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR NOT NULL,
            price FLOAT NOT NULL,
            count INTEGER NOT NULL,
            description VARCHAR NOT NULL
        )
    ''')
    
    # 2. Копируем данные, для description ставим значение по умолчанию
    op.execute('''
        INSERT INTO products_new (id, title, price, count, description)
        SELECT id, title, price, count, 'no description' FROM products
    ''')
    
    # 3. Удаляем старую таблицу
    op.execute('DROP TABLE products')
    
    # 4. Переименовываем новую
    op.execute('ALTER TABLE products_new RENAME TO products')


def downgrade() -> None:
    # Откат: удаляем description
    op.execute('''
        CREATE TABLE products_old (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR NOT NULL,
            price FLOAT NOT NULL,
            count INTEGER NOT NULL
        )
    ''')
    
    op.execute('''
        INSERT INTO products_old (id, title, price, count)
        SELECT id, title, price, count FROM products
    ''')
    
    op.execute('DROP TABLE products')
    op.execute('ALTER TABLE products_old RENAME TO products')