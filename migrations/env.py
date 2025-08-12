from alembic import context
from sqlalchemy import engine_from_config, pool
from app.db_config import Base, SQLALCHEMY_DATABASE_URL

config = context.config
target_metadata = Base.metadata

def _get_url():
    return SQLALCHEMY_DATABASE_URL or config.get_main_option("sqlalchemy.url")

def run_migrations_offline():
    url = _get_url()
    assert url, "No database URL configured"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    url = _get_url()
    assert url, "No database URL configured"
    connectable = engine_from_config(
        {**config.get_section(config.config_ini_section, {}), "sqlalchemy.url": url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()