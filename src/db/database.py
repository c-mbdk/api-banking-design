from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import ClassVar, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.settings import AppSettings, get_app_settings
from src.logger import logger
from src.models.banking_models import Account, Customer, CustomerAccountLink, SQLModel

_DATABASE_CLIENT: Optional["DatabaseClient"] = None


class DatabaseClient:
    """
    Singleton class for Database Client.

    Ensures only one instance of the database client is
    initialised and reused throughout the application.

    Class Attributes:
    _engine: SQLAlchemy engine instance.
    _session_factory: Async session factory.
    """

    _engine: ClassVar[Optional[AsyncEngine]] = None
    _session_factory: Optional[sessionmaker[AsyncSession]] = None

    def __init__(self) -> None:
        """Initialise database client with no configuration."""
        self._initialised = False
        self._app_settings: Optional[AppSettings] = None

    async def initialise(self):
        """Initialise the database client, setting its engine and session factory."""
        if not self._initialised:
            self._app_settings = get_app_settings()
            self._create_pool()
            await self._create_tables()
            self._initialised = True

    def _create_pool(self):
        """Create session factory and connection pool for db connections."""
        self._engine = create_async_engine(
            url=self._app_settings.DATABASE_URL, echo=True
        )
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def _create_tables(self):
        """Create tables defined in the application."""
        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    @asynccontextmanager
    async def get_session(self) -> AbstractAsyncContextManager[AsyncSession]:
        """Create database session for use."""
        session: AsyncSession = self._session_factory()

        try:
            yield session
        except Exception as e:
            logger.exception(f"Session rollback because of exception: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_database_client() -> DatabaseClient:
    """
    Initialises database client to be reused throughout the application.
    """
    global _DATABASE_CLIENT

    if _DATABASE_CLIENT is None:
        _DATABASE_CLIENT = DatabaseClient()
        await _DATABASE_CLIENT.initialise()
        logger.debug("Created and initialised new DatabaseClient.")

    return _DATABASE_CLIENT
