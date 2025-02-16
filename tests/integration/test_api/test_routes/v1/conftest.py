import pytest
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio.engine import AsyncConnection

# from src.api.v1.
from src.db.database import DatabaseClient, get_database_client
from src.enums.account_status import AccountStatus
from src.models.banking_models import SQLModel
from src.repositories.customer_repository import CustomerRepository
from src.schemas.account.account_input import AccountInput
from src.schemas.customer.customer_input import CustomerInput


def verify_db_tables(conn: AsyncConnection) -> bool:
    """Returns boolean to confirm if tables exist in db."""
    inspector = inspect(conn)
    return inspector.has_table("account") and inspector.has_table("customer")

@pytest.fixture(autouse=True)
async def new_db_client() -> DatabaseClient:
    """Fixture to provide the database client for tests."""
    # Setup - for db
    db_client = await get_database_client()

    async with db_client._engine.begin() as conn:
        if not await conn.run_sync(verify_db_tables):
            await conn.run_sync(SQLModel.metadata.create_all)

    yield db_client

    # Teardown
    async with db_client._engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
def valid_customer_data_two():
    """Fixture to provide valid customer data for testing"""
    return [
        {
            "guid": "3566661b-bba9-4bd0-a82c-2966c34db25f",
            "first_name": "Jamie",
            "last_name": "Bloggs",
            "date_of_birth": "1999-09-13",
            "phone_number": "07712 345678",
            "email_address": "jamie.bloggs@gmails.com",
            "address": "123 Barnes Street, London, W17 4DD",
        },
        {
            "guid": "b7630c77-412e-4fbd-9ee2-ac043002e0d1",
            "first_name": "Jillian",
            "middle_names": "Alice",
            "last_name": "Doe",
            "date_of_birth": "1992-01-01",
            "phone_number": "07123 456789",
            "email_address": "jilian.alice.doe@gmails.com",
            "address": "90 East Road, London, E12 4OL",
        },
    ]


@pytest.fixture
def valid_account_data():
    """Fixture to provide valid account data for tests"""
    return {
        "guid": "3c697d53-9902-441b-8d6f-95f7d57638a4",
        "account_name": "Test Account ABC",
        "status": AccountStatus.ACTIVE,
    }


@pytest.fixture
async def seed_db_customer_account(
    new_db_client, valid_customer_data_two, valid_account_data
):
    """Fixture to seed database with valid test data."""

    customer_data = CustomerInput(**valid_customer_data_two[0])
    account_data = AccountInput(**valid_account_data)

    customer_repo = CustomerRepository(new_db_client)
    new_customer = await customer_repo.create(customer_data, account_data)

    return new_customer


@pytest.fixture
def valid_input_customer_account_data(
    valid_customer_data_two, valid_account_data
):
    """Fixture to provide valid data for POST /customers request."""

    return {
        "customer_guid": valid_customer_data_two[0]["guid"],
        "first_name": valid_customer_data_two[0]["first_name"],
        "last_name": valid_customer_data_two[0]["last_name"],
        "date_of_birth": valid_customer_data_two[0]["date_of_birth"],
        "email_address": valid_customer_data_two[0]["email_address"],
        "phone_number": valid_customer_data_two[0]["phone_number"],
        "address": valid_customer_data_two[0]["address"],
        "account_guid": valid_account_data["guid"],
        "account_name": valid_account_data["account_name"],
        "account_status": valid_account_data["status"],
    }