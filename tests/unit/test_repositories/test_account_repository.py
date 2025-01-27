from unittest.mock import MagicMock

import pytest

from src.db.database import DatabaseClient
from src.repositories.account_repository import (
    AccountRepository, get_account_repository
)
from src.schemas.account.account_update import AccountUpdate


@pytest.mark.asyncio
class TestAccountRepository:
    """Test suite for Account Repository."""

    async def test_account_repository_retrieve_all_success(
        self,
        in_memory_db_client,
        customer_in_memory_db,
        valid_account_data,
        valid_customer_data_two
    ):
        """Tests happy path of get all method of AccountRepository"""

        account_repo = AccountRepository(in_memory_db_client)
        all_accounts = await account_repo.get_all()

        assert len(all_accounts) == 1

        account_record = all_accounts[0]

        for field in ["account_name", "status"]:
            assert getattr(account_record, field) == valid_account_data[field]

        assert str(account_record.guid) == valid_account_data["guid"]

        customer_record = account_record.customers[0]

        for field in [
            "first_name", 
            "middle_names", 
            "last_name", 
            "phone_number", 
            "email_address", 
            "address"
            ]:
            assert getattr(customer_record, field) == valid_customer_data_two[0][field]


        assert str(customer_record.guid) == valid_customer_data_two[0]["guid"]

        assert customer_record.date_of_birth.strftime("%Y-%m-%d") == valid_customer_data_two[0]["date_of_birth"]  # noqa


    async def test_get_account_by_guid_success(
        self,
        in_memory_db_client,
        customer_in_memory_db,
        valid_account_data,
        valid_customer_data_two
    ):
        """Tests account record can be successfully retrieved with the guid."""

        account_repo = AccountRepository(in_memory_db_client)
        account_guid = customer_in_memory_db.accounts[0].guid
        retrieved_account = await account_repo.get_by_guid(account_guid)

        assert len(retrieved_account) == 1

        account_record = retrieved_account[0]

        for field in ["account_name", "status"]:
            assert getattr(account_record, field) == valid_account_data[field]

        assert str(account_record.guid) == valid_account_data["guid"]

        customer_record = account_record.customers[0]

        for field in [
            "first_name", 
            "middle_names", 
            "last_name", 
            "phone_number", 
            "email_address", 
            "address"
            ]:
            assert getattr(customer_record, field) == valid_customer_data_two[0][field]


        assert str(customer_record.guid) == valid_customer_data_two[0]["guid"]

        assert customer_record.date_of_birth.strftime("%Y-%m-%d") == valid_customer_data_two[0]["date_of_birth"]  # noqa
    

    async def test_update_account_success(
        self,
        in_memory_db_client,
        customer_in_memory_db,
        valid_account_data
    ):
        """Tests account record can be successfully updated."""

        updated_data = {
            "account_name": "Test Account 123"
        }

        data = AccountUpdate(**updated_data)

        account_repo = AccountRepository(in_memory_db_client)
        account_guid = customer_in_memory_db.accounts[0].guid
        updated_account = await account_repo.update(account_guid, data)

        assert len(updated_account) == 1

        account_record = updated_account[0]

        assert account_record.guid == account_guid
        assert account_record.account_name == updated_data["account_name"]
        assert account_record.status == valid_account_data["status"]

    async def test_delete_account_success(
        self,
        in_memory_db_client,
        customer_in_memory_db
    ):
        """Tests account record successfully deleted."""

        existing_account_guid = customer_in_memory_db.accounts[0].guid
        account_repo = AccountRepository(in_memory_db_client)

        assert await account_repo.delete(existing_account_guid)

    
    async def test_account_exists_by_guid_success(
        self,
        in_memory_db_client,
        customer_in_memory_db
    ):
        """
        Tests checking db for existing account guid will return False.
        """
        account_repo = AccountRepository(in_memory_db_client)
        existing_account_guid = customer_in_memory_db.accounts[0].guid

        assert await account_repo.account_exists_by_guid(existing_account_guid)

    
    async def test_account_exists_by_guid_failure(
        self,
        in_memory_db_client,
        customer_in_memory_db
    ):
        """
        Tests checking db for nonexistent account guid will return False.
        """
        account_repo = AccountRepository(in_memory_db_client)
        nonexistent_account_guid = "20961a8f-ccdc-4452-a301-893129d09458"

        assert await account_repo.account_exists_by_guid(nonexistent_account_guid) is False  # noqa


    async def test_get_account_repository_instance(self):
        """Tests dependency provider for AccountRepository."""

        mock_db_client = MagicMock(spec=DatabaseClient)

        customer_repo = await get_account_repository(mock_db_client)

        assert isinstance(customer_repo, AccountRepository)
        assert customer_repo._db == mock_db_client
