from contextlib import _AsyncGeneratorContextManager
from unittest.mock import AsyncMock, Mock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.db.database import DatabaseClient


@pytest.fixture
def connection_url() -> str:
    """Fixture providing connection URL."""
    return "sqlite:///test.db"
    

@pytest.fixture
def mock_engine() -> AsyncMock:
    """Fixture providing a mocked Async SQLAlchemy engine."""
    return AsyncMock(spec=AsyncEngine)


@pytest.fixture
def mock_session_factory(mock_engine) -> sessionmaker:
    """Fixture providing a mocked session factory."""
    return sessionmaker(bind=mock_engine, class_=AsyncSession, expire_on_commit=False)


class TestDatabaseClient:
    """Test suite for DatabaseClient class."""

    def test_init_successful(self):
        """Test database initialisation."""
        db = DatabaseClient()

        assert db._initialised is False
        assert db._engine is None
        assert db._session_factory is None
        assert db._app_settings is None
    
    @pytest.mark.asyncio
    @patch("src.db.database.get_app_settings")
    @patch("src.db.database.create_async_engine")
    @patch("src.db.database.sessionmaker")
    @patch("src.db.database.SQLModel")
    async def test_initialise_creates_async_engine_and_tables(
        self, 
        mock_sqlmodel,
        mock_sessionmaker, 
        mock_create_engine, 
        mock_get_app_settings, 
        connection_url,
        mock_engine,
        mock_session_factory
    ):
        """Test initialise logic - DatabaseClient instance not initialised."""
        mock_app_settings = Mock()
        mock_app_settings.DATABASE_URL = connection_url
        mock_get_app_settings.return_value = mock_app_settings

        mock_sqlmodel.metadata.return_value = Mock()

        mock_connection = AsyncMock()
        mock_engine.begin.return_value = mock_connection
        mock_create_engine.return_value = mock_engine
        mock_sessionmaker.return_value = mock_session_factory

        db = DatabaseClient()
        
        assert db._initialised is False
        assert db._engine is None
        assert db._session_factory is None
        assert db._app_settings is None
        
        await db.initialise()

        assert db._engine == mock_engine
        assert db._session_factory == mock_session_factory
        assert db._app_settings == mock_app_settings
        assert db._initialised is True

        mock_engine.begin.assert_called_once()
        mock_create_engine.assert_called_once_with(url=connection_url, echo=True)


    @patch("src.db.database.get_app_settings")
    @patch("src.db.database.create_async_engine")
    @patch("src.db.database.sessionmaker")
    @patch("src.db.database.SQLModel")
    def test_initialised_already(
        self,
        mock_sqlmodel,
        mock_sessionmaker,
        mock_create_engine,
        mock_get_app_settings,
        mock_engine,
        mock_session_factory
    ):
        """Tests initialise logic - DatabaseClient already initialised."""

        mock_app_settings = Mock()
        mock_get_app_settings.return_value = mock_app_settings

        mock_sqlmodel.metadata.return_value = Mock()

        mock_connection = AsyncMock()
        mock_engine.begin.return_value = mock_connection
        mock_create_engine.return_value = mock_engine
        mock_sessionmaker.return_value = mock_session_factory

        db = DatabaseClient()

        db._initialised = True

        mock_create_engine.assert_not_called()
        mock_sessionmaker.assert_not_called()
        mock_engine.begin.assert_not_called()


    @pytest.mark.asyncio
    async def test_get_session_successful(
        self, mock_session_factory
    ):
        """Tests session creation of DatabaseClient instance."""

        db = DatabaseClient()
        db._session_factory = mock_session_factory

        session = db.get_session()

        assert isinstance(session, _AsyncGeneratorContextManager)
