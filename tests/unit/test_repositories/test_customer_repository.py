from unittest.mock import MagicMock

import pytest

from src.db.database import DatabaseClient
from src.repositories.customer_repository import (
    CustomerRepository,
    get_customer_repository,
)
from src.schemas.account.account_input import AccountInput
from src.schemas.customer.customer_input import CustomerInput
from src.schemas.customer.customer_update import CustomerUpdate


@pytest.mark.asyncio
class TestCustomerRepository:
    """Test suite for Customer Repository."""

    async def test_customer_repository_retrieve_all_success(
        self,
        in_memory_db_client,
        customer_in_memory_db,
        valid_customer_data_two,
        valid_account_data,
    ):
        """Tests happy path of get all method of CustomerRepository"""

        customer_repo = CustomerRepository(in_memory_db_client)

        all_customers = await customer_repo.get_all()

        assert len(all_customers) == 1

        customer_record = all_customers[0]

        for field in [
            "first_name",
            "middle_names",
            "last_name",
            "phone_number",
            "email_address",
            "address",
        ]:
            assert getattr(customer_record, field) == valid_customer_data_two[0][field]

        assert str(customer_record.guid) == valid_customer_data_two[0]["guid"]

        assert (
            customer_record.date_of_birth.strftime("%Y-%m-%d")
            == valid_customer_data_two[0]["date_of_birth"]
        )  # noqa

        account_record = customer_record.accounts[0]

        for field in ["account_name", "status"]:
            assert getattr(account_record, field) == valid_account_data[field]

        assert str(account_record.guid) == valid_account_data["guid"]

    async def test_get_customer_by_guid_success(
        self,
        in_memory_db_client,
        customer_in_memory_db,
        valid_customer_data_two,
        valid_account_data,
    ):
        """Tests customer record can be successfully retrieved with the guid."""

        customer_repo = CustomerRepository(in_memory_db_client)
        retrieved_customer = await customer_repo.get_by_guid(customer_in_memory_db.guid)

        assert len(retrieved_customer) == 1

        customer_record = retrieved_customer[0]

        for field in [
            "first_name",
            "middle_names",
            "last_name",
            "phone_number",
            "email_address",
            "address",
        ]:
            assert getattr(customer_record, field) == valid_customer_data_two[0][field]

        assert str(customer_record.guid) == valid_customer_data_two[0]["guid"]

        assert (
            customer_record.date_of_birth.strftime("%Y-%m-%d")
            == valid_customer_data_two[0]["date_of_birth"]
        )  # noqa

        account_record = customer_record.accounts[0]

        for field in ["account_name", "status"]:
            assert getattr(account_record, field) == valid_account_data[field]

        assert str(account_record.guid) == valid_account_data["guid"]

    async def test_create_customer_success(
        self,
        in_memory_db_client,
        customer_in_memory_db,
        valid_customer_data_two,
        valid_account_data,
    ):
        """Tests customer record can be successfully created."""

        new_account_data = valid_account_data.copy()
        new_account_data["guid"] = "098b7993-2e83-4dca-bf03-629ef8846151"
        new_account_data["account_name"] = "Test Account DEF"

        customer_data = CustomerInput(**valid_customer_data_two[1])
        account_data = AccountInput(**new_account_data)

        customer_repo = CustomerRepository(in_memory_db_client)
        new_customer = await customer_repo.create(customer_data, account_data)
        new_customer_record = new_customer[0]

        assert new_customer_record != customer_in_memory_db

        for field in [
            "first_name",
            "middle_names",
            "last_name",
            "phone_number",
            "email_address",
            "address",
        ]:
            assert getattr(new_customer_record, field) == valid_customer_data_two[1][field]

        assert str(new_customer_record.guid) == valid_customer_data_two[1]["guid"]

        assert (
            new_customer_record.date_of_birth.strftime("%Y-%m-%d")
            == valid_customer_data_two[1]["date_of_birth"]
        )  # noqa

        account_record = new_customer_record.accounts[0]

        for field in ["account_name", "status"]:
            assert getattr(account_record, field) == new_account_data[field]

        assert str(account_record.guid) == new_account_data["guid"]

    async def test_update_customer_success(
        self,
        in_memory_db_client,
        customer_in_memory_db,
        valid_customer_data_two,
        valid_account_data,
    ):
        """Tests customer record can be successfully updated."""

        updated_data = {
            "middle_names": "Andrew Nathan",
            "email_address": "joe.a.n.bloggs@email.com",
        }
        data = CustomerUpdate(**updated_data)

        customer_repo = CustomerRepository(in_memory_db_client)
        updated_customer = await customer_repo.update(customer_in_memory_db.guid, data)

        assert len(updated_customer) == 1

        customer_record = updated_customer[0]

        for field in updated_data.keys():
            assert getattr(customer_record, field) == updated_data[field]

        for field in ["first_name", "last_name", "phone_number", "address"]:
            assert getattr(customer_record, field) == valid_customer_data_two[0][field]

        assert str(customer_record.guid) == valid_customer_data_two[0]["guid"]

        assert (
            customer_record.date_of_birth.strftime("%Y-%m-%d")
            == valid_customer_data_two[0]["date_of_birth"]
        )  # noqa

        account_record = customer_record.accounts[0]

        for field in ["account_name", "status"]:
            assert getattr(account_record, field) == valid_account_data[field]

        assert str(account_record.guid) == valid_account_data["guid"]

    async def test_delete_customer_success(
        self,
        in_memory_db_client,
        customer_in_memory_db,
    ):
        """Tests customer record successfully deleted."""

        existing_customer_guid = customer_in_memory_db.guid
        customer_repo = CustomerRepository(in_memory_db_client)

        assert await customer_repo.delete(existing_customer_guid)

    async def test_customer_exists_by_guid_success(
        self, in_memory_db_client, customer_in_memory_db
    ):
        """
        Tests check db for existing customer guid will return True.
        """
        customer_repo = CustomerRepository(in_memory_db_client)

        assert await customer_repo.customer_exists_by_guid(customer_in_memory_db.guid)

    async def test_customer_exists_by_guid_fail(
        self, in_memory_db_client, customer_in_memory_db
    ):
        """
        Tests checking db for nonexistent customer guid will return False.
        """
        customer_repo = CustomerRepository(in_memory_db_client)
        nonexistent_customer_guid = "6e7e9655-c6ad-4069-80a6-2c6bb6cd114e"

        assert (
            await customer_repo.customer_exists_by_guid(nonexistent_customer_guid)
            is False
        )  # noqa

    async def test_get_customer_repository_instance(self):
        """Tests dependency provider for CustomerRepository."""

        mock_db_client = MagicMock(spec=DatabaseClient)

        customer_repo = await get_customer_repository(mock_db_client)

        assert isinstance(customer_repo, CustomerRepository)
        assert customer_repo._db == mock_db_client
