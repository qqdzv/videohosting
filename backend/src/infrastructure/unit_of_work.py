from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        return self

    async def __aexit__(self, exc_type: object, *_: object) -> None:
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
