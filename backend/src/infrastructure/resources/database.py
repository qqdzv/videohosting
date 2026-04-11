from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import (
    PostgresConfig,
)


def new_db_session_maker(psql_config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        psql_config.url,
        pool_size=5,
        echo=False,
    )
    return async_sessionmaker(engine)
