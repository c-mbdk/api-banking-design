import json

import pytest

from src.enums.account_status import AccountStatus
from src.schemas.account.account_output import AccountOutput
from src.schemas.account.account_update import AccountUpdate
from src.schemas.base_response import GenericResponseModel
from src.schemas.customer.customer_output import CustomerOutput
from src.services.account_service import AccountService, get_account_service


@pytest.mark.asyncio
class TestAccountService:
    """Test suite for AccountService."""

    @pytest.fixture
    def account_service_with_repo(mock_db_client, mock_account_repository):
        """
        Fixture providing instance of AccountService with mock account repo.
        """

        account_service = AccountService(mock_db_client)
        account_service.account_repository = mock_account_repository

        return account_service, mock_account_repository

    async def test_retrieve_all_success(self, account_service_with_repo):
        """Tests happy path of get all method of AccountService."""

        account_service, mock_account_repository = account_service_with_repo

        mock_repo_output = [
            AccountOutput(
                guid="b7faf352-8e6e-4e7d-827e-ab6272234cb2",
                account_name="Current Account - Jay",
                status=AccountStatus.ACTIVE,
                customers=[
                    CustomerOutput(
                        guid="011aed67-3bb3-4b21-9a86-89da92bd6281",
                        first_name="Jay",
                        middle_names="Nathan",
                        last_name="Bloggs",
                        date_of_birth="1985-04-11",
                        phone_number="07112233445",
                        email_address="jay.nathan.bloggs@email.com",
                        address="99 Zoo Lane, Manchester, M12 4FG",
                    )
                ],
            )
        ]

        mock_account_repository.get_all.return_value = mock_repo_output

        all_accounts = await account_service.get_all()

        assert isinstance(all_accounts, GenericResponseModel)
        expected_response_attrs = {
            "status_code": 200,
            "success": "true",
            "message": "Available account data returned",
            "data": [account.model_dump_json() for account in mock_repo_output],
        }

        for field in expected_response_attrs.keys():
            assert getattr(all_accounts, field) == expected_response_attrs[field]

        mock_account_repository.get_all.assert_called_once()

    async def test_retrieve_single_account_success(self, account_service_with_repo):
        """Tests happy path of get_account method of AccountService."""

        account_service, mock_account_repository = account_service_with_repo

        test_account_guid = "839b787a-0c2d-4088-b485-df28f4b13452"
        test_customer_guid = "050b326b-1948-4f58-abfa-57fa2ae5a720"

        mock_repo_output = [
            AccountOutput(
                guid=test_account_guid,
                account_name="Current Account - Jonathan",
                status=AccountStatus.ACTIVE,
                customers=[
                    CustomerOutput(
                        guid=test_customer_guid,
                        first_name="Jonathan",
                        middle_names="Thomas",
                        last_name="Bloggs",
                        date_of_birth="1995-07-19",
                        phone_number="07112565656",
                        email_address="jonathan.thomas.bloggs@email.com",
                        address="100 East Street, Liverpool, L1 0RT",
                    )
                ],
            )
        ]

        mock_account_repository.get_by_guid.return_value = mock_repo_output
        mock_account_repository.account_exists_by_guid.return_value = True

        retrieved_account = await account_service.get_account(test_account_guid)

        assert isinstance(retrieved_account, GenericResponseModel)
        expected_response_attrs = {
            "status_code": 200,
            "success": "true",
            "message": "Available account data returned",
            "data": [account.model_dump_json() for account in mock_repo_output],
        }
        for field in expected_response_attrs.keys():
            assert getattr(retrieved_account, field) == expected_response_attrs[field]

        mock_account_repository.get_by_guid.assert_called_once()

    async def test_retrieve_single_account_failure(self, account_service_with_repo):
        """Tests unhappy path of get_account method of AccountService."""

        account_service, mock_account_repository = account_service_with_repo

        test_account_guid = "02308a1b-781c-4f19-967f-acd957218fab"

        mock_account_repository.account_exists_by_guid.return_value = False
        mock_account_repository.get_by_guid.return_value = None

        with pytest.raises(Exception) as exc_info:
            retrieved_account = await account_service.get_account(test_account_guid)

            assert not isinstance(retrieved_account, GenericResponseModel)

        assert str(exc_info.value.detail) == f"Account not found: {test_account_guid}"
        assert str(exc_info.value.status_code) == "404"

        mock_account_repository.account_exists_by_guid.assert_called_once()
        mock_account_repository.get_by_guid.assert_not_called()

    async def test_delete_account_success(self, account_service_with_repo):
        """Tests happy path of delete method of AccountService."""

        account_service, mock_account_repository = account_service_with_repo

        test_account_guid = "cc57841a-5719-4144-91f6-0c2b912822f3"

        mock_account_repository.account_exists_by_guid.return_value = True
        mock_account_repository.delete.return_value = True

        account_deleted = await account_service.delete(test_account_guid)

        assert isinstance(account_deleted, GenericResponseModel)

        expected_response_attrs = {
            "status_code": 200,
            "success": "true",
            "message": "Account record deleted",
            "data": [],
        }

        for field in expected_response_attrs.keys():
            assert getattr(account_deleted, field) == expected_response_attrs[field]

        mock_account_repository.delete.assert_called_once()
        mock_account_repository.account_exists_by_guid.assert_called_once()

    async def test_delete_account_not_found(self, account_service_with_repo):
        """
        Tests unhappy path of delete method of AccountService - nonexistent account.
        """

        account_service, mock_account_repository = account_service_with_repo

        test_account_guid = "2784ad92-b250-494f-b8cc-3ce09e810be2"

        mock_account_repository.account_exists_by_guid.return_value = False
        mock_account_repository.delete.return_value = None

        with pytest.raises(Exception) as exc_info:
            account_deleted = await account_service.delete(test_account_guid)

            assert not isinstance(account_deleted, GenericResponseModel)

        assert str(exc_info.value.status_code) == "404"
        assert str(exc_info.value.detail) == f"Account not found: {test_account_guid}"

        mock_account_repository.account_exists_by_guid.assert_called_once()
        mock_account_repository.delete.assert_not_called()

    async def test_delete_account_failure_server_error(self, account_service_with_repo):
        """
        Tests unhappy path of delete method of AccountService - deletion fails.
        """

        account_service, mock_account_repository = account_service_with_repo

        test_account_guid = "cf82c0fd-0e9a-4c05-bdb7-556540ec63fc"

        mock_account_repository.account_exists_by_guid.return_value = True
        mock_account_repository.delete.return_value = False

        account_deleted = await account_service.delete(test_account_guid)

        assert isinstance(account_deleted, GenericResponseModel)

        expected_response_attrs = {
            "status_code": 500,
            "success": "false",
            "message": f"Account record not deleted: {test_account_guid}",
            "data": [],
        }

        for field in expected_response_attrs.keys():
            assert getattr(account_deleted, field) == expected_response_attrs[field]

        mock_account_repository.account_exists_by_guid.assert_called_once()
        mock_account_repository.delete.assert_called_once()

    async def test_update_account_success(self, account_service_with_repo):
        """Tests happy path of update method of AccountService."""

        account_service, mock_account_repository = account_service_with_repo

        test_account_guid = "1e495145-390c-489a-b2a8-49bf2a34bb39"
        test_customer_guid = "12ffedb4-06f2-422c-a420-b16d80ae6fb8"

        mock_repo_output = [
            AccountOutput(
                guid=test_account_guid,
                account_name="Current Account - J.A. Bloggs",
                status=AccountStatus.ACTIVE,
                customers=[
                    CustomerOutput(
                        guid=test_customer_guid,
                        first_name="Jason",
                        middle_names="Andrew",
                        last_name="Bloggs",
                        date_of_birth="1998-09-23",
                        phone_number="07112787878",
                        email_address="jason.andrew.bloggs@email.com",
                        address="101 Moors Street, Derby, DE1 3PT",
                    )
                ],
            )
        ]

        mock_account_repository.account_exists_by_guid.return_value = True
        mock_account_repository.update.return_value = mock_repo_output

        update_data = AccountUpdate(account_name="Current Account - J.A. Bloggs")

        expected_resp_attrs = {
            "status_code": 200,
            "success": "true",
            "message": "Account record updated",
            "data": [account.model_dump_json() for account in mock_repo_output],
        }

        updated_account_resp = await account_service.update(
            test_account_guid, update_data
        )

        for field in expected_resp_attrs.keys():
            assert getattr(updated_account_resp, field) == expected_resp_attrs[field]

        account_record = json.loads(updated_account_resp.data[0])

        assert account_record["account_name"] == "Current Account - J.A. Bloggs"

        mock_account_repository.update.assert_called_once()
        mock_account_repository.account_exists_by_guid.assert_called_once()

    async def test_get_account_service_provider(self, mock_account_repository):
        """Tests dependency provider for AccountRepository."""

        account_service = await get_account_service(mock_account_repository)

        assert isinstance(account_service, AccountService)
        assert account_service.account_repository == mock_account_repository
