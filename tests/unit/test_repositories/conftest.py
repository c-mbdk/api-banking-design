from unittest.mock import Mock, patch

import pytest

from src.db.database import DatabaseClient
from src.enums.account_status import AccountStatus
from src.repositories.customer_repository import CustomerRepository
from src.schemas.account.account_input import AccountInput
from src.schemas.customer.customer_input import CustomerInput
from tests.shared.constants import TEST_GUID_1, TEST_GUID_2


@pytest.fixture
def valid_customer_data_two():
    """Fixture to provide valid customer data for testing"""
    return [
        {
            "guid": TEST_GUID_1,
            "first_name": "Joe",
            "middle_names": "Andrew",
            "last_name": "Bloggs",
            "date_of_birth": "1997-07-17",
            "phone_number": "07712 345678",
            "email_address": "joe.bloggs@gmails.com",
            "address": "123 Baker Street, London, W12 344",
        },
        {
            "guid": TEST_GUID_2,
            "first_name": "Jane",
            "middle_names": "Alice",
            "last_name": "Doe",
            "date_of_birth": "1994-03-21",
            "phone_number": "07123 456789",
            "email_address": "jane.alice.doe@gmails.com",
            "address": "90 East Street, London, E12 345",
        },
    ]


@pytest.fixture
def valid_account_data():
    """Fixture to provide valid account data for tests"""
    return {
        "guid": "9f241ec8-802d-4562-9718-2131f963c64d",
        "account_name": "Test Account ABC",
        "status": AccountStatus.ACTIVE,
    }



@pytest.fixture
@patch("src.db.database.get_app_settings")
async def in_memory_db_client(mock_get_app_settings):
    mock_app_settings = Mock()
    mock_app_settings.DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    mock_get_app_settings.return_value = mock_app_settings

    db_client = DatabaseClient()
    await db_client.initialise()

    return db_client


@pytest.fixture
async def customer_in_memory_db(
    in_memory_db_client, valid_account_data, valid_customer_data_two
):
    """
    Fixture to provide CustomerRepository with customer data.
    """

    customer_data = CustomerInput(**valid_customer_data_two[0])
    account_data = AccountInput(**valid_account_data)

    customer_repo = CustomerRepository(in_memory_db_client)
    new_customer = await customer_repo.create(customer_data, account_data)

    return new_customer[0]
