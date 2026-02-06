import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# backend 폴더를 path에 추가하여 app 모듈을 찾을 수 있게 함
sys.path.append(os.getcwd())

# Config 객체
config = context.config

# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ===== App 설정 로드 =====
from app.core.config import settings
# Alembic config에 DATABASE_URL 주입
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# 메타데이터 타겟 설정
from app.db.base import Base
# 모든 모델을 import 해야 Base.metadata에 등록됨
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.store import Store
from app.models.user_store import UserStore
from app.models.stock import CurrentStock
from app.models.transaction import InventoryTransaction

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
