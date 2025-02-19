from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from core.config import Settings  # Ensure the correct import path
from database import Base

# Import your models
from models import track

# Logging configuration
from logging.config import fileConfig

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Database URL and Metadata
settings = Settings()
db_url = str(settings.ASYNC_DATABASE_URI)
target_metadata = Base.metadata

# Migration Functions
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(db_url)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
