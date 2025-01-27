from datetime import date
import json

import pytest

from src.enums.account_status import AccountStatus
from src.models.banking_models import Account, Customer
from src.schemas.base_response import GenericResponseModel
from src.schemas.account.account_output import AccountOutput
from src.schemas.create_customer_request import CreateCustomerRequest
from src.schemas.customer.customer_output import CustomerOutput
from src.schemas.customer.customer_update import CustomerUpdate
from src.services.customer_service import CustomerService, get_customer_service
from tests.shared.constants import TEST_GUID_3, TEST_GUID_4


@pytest.mark.asyncio
class TestCustomerService:
    """Test suite for CustomerService."""

    @pytest.fixture
    def customer_service_with_repo(mock_db_client, mock_customer_repository):
        """
        Fixture providing instance of CustomerService with mock contact repo.
        """
        customer_service = CustomerService(mock_db_client)
        customer_service.customer_repository = mock_customer_repository

        return customer_service, mock_customer_repository

    async def test_retrieve_all_success(self, customer_service_with_repo):
        """Tests happy path of get all method of CustomerService."""
        
        customer_service, mock_customer_repository = customer_service_with_repo

        mock_repo_output = [
            CustomerOutput(
                guid=TEST_GUID_3,
                first_name="Jacqueline",
                middle_names="Anita",
                last_name="Doe",
                date_of_birth="1994-03-24",
                phone_number="07123456789",
                email_address="jacqueline.a.doe@email.com",
                address="123 Baker Street, London, EC3M 6DD",
                accounts=[
                    AccountOutput(
                        guid=TEST_GUID_4,
                        account_name="Current Account - Jacqueline",
                        status=AccountStatus.ACTIVE
                    )
                ]
            )
        ]

        mock_customer_repository.get_all.return_value = mock_repo_output

        all_customers = await customer_service.get_all()

        assert isinstance(all_customers, GenericResponseModel)
        expected_response_attrs = {
            "status_code": 200,
            "success": "true",
            "message": "Available customer data returned",
            "data": [customer.model_dump_json() for customer in mock_repo_output]
        }
        for field in expected_response_attrs.keys():
            assert getattr(all_customers, field) == expected_response_attrs[field]
        
        mock_customer_repository.get_all.assert_called_once()


    async def test_retrieve_single_customer_success(self, customer_service_with_repo):
        """Tests happy path of get_customer method of CustomerService"""

        customer_service, mock_customer_repository = customer_service_with_repo

        test_customer_guid = "365fe999-4781-40c7-a7b2-35c3800bb4c3"
        test_account_guid = "77fbf3fa-3418-4e1c-85de-44fcf06daee0"

        mock_repo_output = [
            CustomerOutput(
                guid=test_customer_guid,
                first_name="Jacqueline",
                middle_names="Anita",
                last_name="Doe",
                date_of_birth="1994-03-24",
                phone_number="07123456789",
                email_address="jacqueline.a.doe@email.com",
                address="123 Baker Street, London, EC3M 6DD",
                accounts=[
                    AccountOutput(
                        guid=test_account_guid,
                        account_name="Current Account - Jacqueline",
                        status=AccountStatus.ACTIVE
                    )
                ]
            )
        ]

        mock_customer_repository.get_by_guid.return_value = mock_repo_output
        mock_customer_repository.customer_exists_by_guid.return_value = True

        retrieved_customer = await customer_service.get_customer(test_customer_guid)

        assert isinstance(retrieved_customer, GenericResponseModel)
        expected_response_attrs = {
            "status_code": 200,
            "success": "true",
            "message": "Available customer data returned",
            "data": [customer.model_dump_json() for customer in mock_repo_output]
        }
        for field in expected_response_attrs.keys():
            assert getattr(retrieved_customer, field) == expected_response_attrs[field]
        
        mock_customer_repository.get_by_guid.assert_called_once()


    async def test_retrieve_single_customer_failure(self, customer_service_with_repo):
        """Tests unhappy path of get_customer method of CustomerService."""

        customer_service, mock_customer_repository = customer_service_with_repo

        test_customer_guid = "a621d452-78cc-4a29-97ad-1aad6949bd3c"

        mock_customer_repository.customer_exists_by_guid.return_value = False
        mock_customer_repository.get_by_guid.return_value = None
        
        with pytest.raises(Exception) as exc_info:
            retrieved_customer = await customer_service.get_customer(test_customer_guid)

            assert not isinstance(retrieved_customer, GenericResponseModel)
        
        assert str(exc_info.value.detail) == f"Customer not found: {test_customer_guid}"
        assert str(exc_info.value.status_code) == "404"

        mock_customer_repository.customer_exists_by_guid.assert_called_once()
        mock_customer_repository.get_by_guid.assert_not_called()


    async def test_delete_customer_success(self, customer_service_with_repo):
        """Tests happy path of delete method of CustomerService."""

        customer_service, mock_customer_repository = customer_service_with_repo

        test_customer_guid = "74cdac7c-fc2b-4684-83ff-027ff4fc0712"

        mock_customer_repository.customer_exists_by_guid.return_value = True
        mock_customer_repository.delete.return_value = True
        
        customer_deleted = await customer_service.delete(test_customer_guid)

        assert isinstance(customer_deleted, GenericResponseModel)

        expected_response_attrs = {
            "status_code": 200,
            "success": "true",
            "message": "Customer record deleted",
            "data": []
        }

        for field in expected_response_attrs.keys():
            assert getattr(customer_deleted, field) == expected_response_attrs[field]
        mock_customer_repository.delete.assert_called_once()
        mock_customer_repository.customer_exists_by_guid.assert_called_once()


    async def test_delete_customer_not_found(self, customer_service_with_repo):
        """
        Tests unhappy path of delete method of CustomerService - nonexistent customer.
        """

        customer_service, mock_customer_repository = customer_service_with_repo

        test_customer_guid = "4fdd08aa-5e21-4363-af91-cbd29f9e89ae"

        mock_customer_repository.customer_exists_by_guid.return_value = False
        mock_customer_repository.delete.return_value = None
        
        with pytest.raises(Exception) as exc_info:
            customer_deleted = await customer_service.delete(test_customer_guid)

            assert not isinstance(customer_deleted, GenericResponseModel)
        
        assert str(exc_info.value.status_code) == "404"
        assert str(exc_info.value.detail) == f"Customer not found: {test_customer_guid}"

        mock_customer_repository.customer_exists_by_guid.assert_called_once()
        mock_customer_repository.delete.assert_not_called()

    
    async def test_delete_customer_failure_server_error(
        self, customer_service_with_repo
    ):
        """
        Tests unhappy path of delete method of CustomerService - deletion fails.
        """

        customer_service, mock_customer_repository = customer_service_with_repo

        test_customer_guid = "9a2b8dc1-be6a-404d-b6eb-2e5e0232c97c"

        mock_customer_repository.customer_exists_by_guid.return_value = True
        mock_customer_repository.delete.return_value = False
        
        customer_deleted = await customer_service.delete(test_customer_guid)

        assert isinstance(customer_deleted, GenericResponseModel)

        expected_response_attrs = {
            "status_code": 500,
            "success": "false",
            "message": f"Customer record not deleted: {test_customer_guid}",
            "data": []
        }

        for field in expected_response_attrs.keys():
            assert getattr(customer_deleted, field) == expected_response_attrs[field]

        mock_customer_repository.customer_exists_by_guid.assert_called_once()
        mock_customer_repository.delete.assert_called_once()

        
    async def test_update_customer_success(self, customer_service_with_repo):
        """Tests happy path of update method of CustomerService."""

        customer_service, mock_customer_repository = customer_service_with_repo

        test_customer_guid = "2f9d04a9-628d-41e3-8dac-330cb6eee59d"

        mock_repo_output = [
            CustomerOutput(
                guid=test_customer_guid,
                first_name="Josephine",
                middle_names="Anu",
                last_name="Doe",
                date_of_birth="1991-08-27",
                phone_number="07123898989",
                email_address="j.a.doe@email.com",
                address="64 Zoo Lane, London, W21 9GG",
                accounts=[
                    AccountOutput(
                        guid="c1248029-11b1-49d0-ab5f-4089f53b3d20",
                        account_name="Current Account - Josephine",
                        status=AccountStatus.ACTIVE
                    )
                ]
            )
        ]

        mock_customer_repository.customer_exists_by_guid.return_value = True
        mock_customer_repository.update.return_value = mock_repo_output

        update_data = CustomerUpdate(
            middle_names="Anu",
            email_address="j.a.doe@email.com"
        )

        expected_resp_attrs = {
            "status_code": 200,
            "success": "true",
            "message": "Customer record updated",
            "data": [customer.model_dump_json() for customer in mock_repo_output]
        }

        updated_customer_resp = await customer_service.update(
            test_customer_guid, update_data
        )

        assert isinstance(updated_customer_resp, GenericResponseModel)

        for field in expected_resp_attrs.keys():
            assert getattr(updated_customer_resp, field) == expected_resp_attrs[field]

        customer_record = json.loads(updated_customer_resp.data[0])

        assert customer_record["middle_names"] == "Anu"
        assert customer_record["email_address"] == "j.a.doe@email.com"
        
        mock_customer_repository.update.assert_called_once()
        mock_customer_repository.customer_exists_by_guid.assert_called_once()


    async def test_update_non_existent_customer(self, customer_service_with_repo):
        """
        Tests unhappy path of update method of CustomerService - nonexistent customer.
        """

        customer_service, mock_customer_repository = customer_service_with_repo

        test_customer_guid = "cd63c6f1-aa5e-484c-8d66-3b4f51c408af"

        mock_customer_repository.customer_exists_by_guid.return_value = False
        mock_customer_repository.update.return_value = None

        update_data = CustomerUpdate(
            middle_names="Barbara"
        )

        with pytest.raises(Exception) as exc_info:
            updated_customer_resp = await customer_service.update(
                test_customer_guid, update_data
            )

            assert not isinstance(updated_customer_resp, GenericResponseModel)


        assert str(exc_info.value.status_code) == "404"
        assert str(exc_info.value.detail) == f"Customer not found: {test_customer_guid}"

        mock_customer_repository.customer_exists_by_guid.assert_called_once()
        mock_customer_repository.update.assert_not_called()

    
    async def test_create_customer_success(self, customer_service_with_repo):
        """Tests create method of CustomerService class."""
        
        customer_service, mock_customer_repository = customer_service_with_repo

        customer_guid = "91ecf55b-12c5-4b89-827f-be06fc5dfa89"
        first_name = "Jaime"
        middle_names = "Annie"
        last_name = "Doe"
        email_address = "jaime.annie.doe@email.com"
        phone_number = "07123565656"
        date_of_birth = date.fromisoformat("1983-03-21")
        address = "33 Turtle Road, Birmingham, B6 3RD"
        account_guid = "e5f28dd6-095f-4e47-a56a-d284419a7f87"
        account_name = "Test Account 1213"
        account_status = AccountStatus.ACTIVE

        mock_repo_output = Customer(
            guid=customer_guid,
            first_name=first_name,
            middle_names=middle_names,
            last_name=last_name,
            email_address=email_address,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            address=address,
            accounts=[Account(
                guid=account_guid,
                account_name=account_name,
                status=account_status
            )]
        )
        mock_customer_repository.create.return_value = mock_repo_output

        input_data = {
            "customer_guid": customer_guid,
            "first_name": first_name,
            "middle_names": middle_names,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "email_address": email_address,
            "phone_number": phone_number,
            "address": address,
            "account_guid": account_guid,
            "account_name": account_name,
            "account_status": account_status
        }

        expected_resp = {
            "status_code": 201,
            "success": "true",
            "message": "Customer record created",
            "data": [CustomerOutput(**mock_repo_output.model_dump()).model_dump_json()]
        }

        new_customer_resp = await customer_service.create(
            CreateCustomerRequest(**input_data)
        )
        
        assert isinstance(new_customer_resp, GenericResponseModel)
        for field in expected_resp.keys():
            assert getattr(new_customer_resp, field) == expected_resp[field]

        mock_customer_repository.create.assert_called_once()


    async def test_get_customer_service_provider(
        self, mock_customer_repository
    ):
        """Tests dependency provider for CustomerRepository."""

        customer_service = await get_customer_service(mock_customer_repository)

        assert isinstance(customer_service, CustomerService)
        assert customer_service.customer_repository == mock_customer_repository
