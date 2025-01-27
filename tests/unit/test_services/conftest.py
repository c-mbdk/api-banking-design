from unittest.mock import MagicMock

import pytest
from sqlmodel import Session

from src.db.database import DatabaseClient
from src.repositories.account_repository import AccountRepository
from src.repositories.customer_repository import CustomerRepository


@pytest.fixture
def mock_db_client():
    """Fixture providing mock db client."""
    return MagicMock(spec=DatabaseClient)


@pytest.fixture
def mock_customer_repository(mock_db_client):
    """Fixture providing mock instance of CustomerRepository."""
    return MagicMock(spec=CustomerRepository(mock_db_client))


@pytest.fixture
def mock_account_repository(mock_db_client):
    """Fixture providing mock instance of AccountRepository."""
    return MagicMock(spec=AccountRepository(mock_db_client))
