from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI, HTTPException
from httpx import ASGITransport, AsyncClient

from src.api.v1.routers.customer import router
from src.schemas.base_response import GenericResponseModel
from src.services.customer_service import CustomerService, get_customer_service
from tests.shared.constants import test_url


class TestCustomerRouter:
    """Test suite for /customers route."""

    @pytest.fixture
    def mock_customer_service(self):
        """Provides mock customer service instance for testing."""
        mock_service = AsyncMock(spec=CustomerService)
        return mock_service

    @pytest.fixture
    def new_customer_request_data(self, mock_customer_account_base):
        """Provides customer request data for testing POST requests."""
        request_data = {
            "customer_guid": mock_customer_account_base.guid,
            "first_name": mock_customer_account_base.first_name,
            "middle_names": mock_customer_account_base.middle_names,
            "last_name": mock_customer_account_base.last_name,
            "date_of_birth": mock_customer_account_base.date_of_birth.strftime(
                "%Y-%m-%d"
            ),
            "phone_number": mock_customer_account_base.phone_number,
            "email_address": mock_customer_account_base.email_address,
            "address": mock_customer_account_base.address,
            "account_guid": mock_customer_account_base.accounts[0].guid,
            "account_name": mock_customer_account_base.accounts[0].account_name,
            "status": mock_customer_account_base.accounts[0].status,
        }

        return request_data

    @pytest.fixture
    def mock_customer_response(self, mock_customer_account_base):
        """Provides base mock response for CustomerService."""
        return GenericResponseModel(
            success="true",
            message="Available customer data returned",
            status_code=200,
            data=[mock_customer_account_base.model_dump()],
        )

    @pytest.fixture(scope="function")
    def test_app(self, mock_customer_service):
        """
        Fixture for app configured with mock customer service.
        """
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_customer_service] = lambda: mock_customer_service

        return app

    @pytest.fixture(scope="function")
    async def client(self, test_app):
        """Fixture for test client."""
        async with AsyncClient(
            transport=ASGITransport(test_app), base_url=test_url
        ) as client:
            yield client

    async def test_create_single_customer_success(
        self,
        mock_customer_service,
        client,
        mock_customer_response,
        new_customer_request_data,
    ):
        """Tests happy path for POST /customers (single)."""

        new_resp_attrs = {"message": "Customer record created", "status_code": 201}
        for key, value in new_resp_attrs.items():
            setattr(mock_customer_response, key, value)

        mock_customer_service.create.return_value = mock_customer_response

        response = await client.post(
            "/customers",
            json=new_customer_request_data,
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 201

        response_json = response.json()
        for field in ["success", "status_code", "message"]:
            assert response_json[field] == getattr(mock_customer_response, field)

        # Assert against customer records returned in data attribute
        resp_data_field_list = list(mock_customer_response.data[0].keys())
        resp_data_field_list.remove("date_of_birth")
        resp_data_field_list.remove("accounts")
        for field in resp_data_field_list:
            assert (
                response_json["data"][0][field] == mock_customer_response.data[0][field]
            )

        assert response_json["data"][0]["date_of_birth"] == mock_customer_response.data[
            0
        ]["date_of_birth"].strftime(
            "%Y-%m-%d"
        )

        for field in response_json["data"][0]["accounts"][0].keys():
            assert (
                response_json["data"][0]["accounts"][0][field]
                == mock_customer_response.data[0]["accounts"][0][field]
            )

    async def test_get_customers_success(
        self,
        mock_customer_service,
        client,
        mock_customer_response,
        mock_customer_account_base,
    ):
        """Tests happy path for GET /customers."""

        mock_customer_service.get_all.return_value = mock_customer_response

        response = await client.get("/customers")

        assert response.status_code == 200

        response_json = response.json()
        for field in ["success", "status_code", "message"]:
            assert response_json[field] == getattr(mock_customer_response, field)

        # Assert against customer records returned in data attribute
        resp_data_field_list = list(mock_customer_response.data[0].keys())
        resp_data_field_list.remove("date_of_birth")
        resp_data_field_list.remove("accounts")
        for field in resp_data_field_list:
            assert (
                response_json["data"][0][field] == mock_customer_response.data[0][field]
            )

        assert response_json["data"][0]["date_of_birth"] == mock_customer_response.data[
            0
        ]["date_of_birth"].strftime(
            "%Y-%m-%d"
        )

        for field in response_json["data"][0]["accounts"][0].keys():
            assert response_json["data"][0]["accounts"][0][field] == getattr(
                mock_customer_account_base.accounts[0], field
            )

    async def test_get_single_customer_success(
        self,
        mock_customer_service,
        client,
        mock_customer_response,
    ):
        """Tests happy path of GET /customers/{guid}"""

        test_customer_guid = "a8258462-03ad-406b-8cc6-d25c7ce96918"

        mock_customer_response.data[0]["guid"] = test_customer_guid

        test_customer_data = {
            "guid": test_customer_guid,
            "first_name": "Jillian",
            "middle_names": "Angela",
            "last_name": "Doe",
            "date_of_birth": "1995-08-31",
            "email_address": "jillian.a.doe@email.com",
            "phone_number": "07123989796",
            "address": "94 Sesame Street, London, S12 P89",
        }

        for key, value in test_customer_data.items():
            mock_customer_response.data[0][key] = value

        test_account_data = {
            "guid": "09d3d017-0f11-4bb4-817f-c4a4c1beb458",
            "account_name": "Current Account - Jillian Doe",
            "status": "Active",
        }

        for key, value in test_account_data.items():
            mock_customer_response.data[0]["accounts"][0][key] = value

        mock_customer_service.get_customer.return_value = mock_customer_response

        response = await client.get(f"/customers/{test_customer_guid}")

        assert response.status_code == 200

        response_json = response.json()
        for field in ["success", "status_code", "message"]:
            assert response_json[field] == getattr(mock_customer_response, field)

        # Assert against customer records returned in data attribute
        resp_customer_data_fields = list(mock_customer_response.data[0].keys())
        resp_customer_data_fields.remove("date_of_birth")
        resp_customer_data_fields.remove("accounts")
        for field in resp_customer_data_fields:
            assert (
                response_json["data"][0][field] == mock_customer_response.data[0][field]
            )

        # Assert against the accounts returned in the customer record returned in datA
        for field in test_account_data.keys():
            assert (
                response_json["data"][0]["accounts"][0][field]
                == test_account_data[field]
            )

        assert (
            response_json["data"][0]["date_of_birth"]
            == test_customer_data["date_of_birth"]
        )

    async def test_get_single_customer_failure(
        self,
        mock_customer_service,
        client,
    ):
        """Tests unhappy path of GET /customers/{guid}."""
        test_customer_guid = "82079432-3f80-4e09-931c-85c56ef163cc"

        mock_customer_service.get_customer.side_effect = HTTPException(
            status_code=404, detail=f"Customer not found: {test_customer_guid}"
        )

        response = await client.get(f"/customers/{test_customer_guid}")

        assert response.status_code == 404
        assert response.json() == {
            "detail": f"Customer not found: {test_customer_guid}"
        }

    async def test_update_customer_successful(
        self, mock_customer_service, client, mock_customer_response
    ):
        """Tests happy path of PUT /customers/{guid}"""

        test_customer_guid = "382635ad-4d67-4657-947a-be2279b87b3d"

        updated_customer_data = {
            "first_name": "Janine",
            "email_address": "janine.a.doe@email.com",
        }

        for key, value in updated_customer_data.items():
            mock_customer_response.data[0][key] = value

        mock_customer_response.message = "Customer record updated"

        mock_customer_service.update.return_value = mock_customer_response

        response = await client.put(
            f"/customers/{test_customer_guid}",
            json=updated_customer_data,
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200

        response_json = response.json()
        for field in ["success", "status_code", "message"]:
            assert response_json[field] == getattr(mock_customer_response, field)

        # Assert against customer records returned in data attribute
        resp_customer_data_fields = list(mock_customer_response.data[0].keys())
        resp_customer_data_fields.remove("date_of_birth")
        resp_customer_data_fields.remove("accounts")
        for field in resp_customer_data_fields:
            assert (
                response_json["data"][0][field] == mock_customer_response.data[0][field]
            )

        # Assert against the accounts returned in the customer record returned in datA
        for field in ["guid", "account_name", "status"]:
            assert (
                response_json["data"][0]["accounts"][0][field]
                == mock_customer_response.data[0]["accounts"][0][field]
            )

        assert response_json["data"][0]["date_of_birth"] == mock_customer_response.data[
            0
        ]["date_of_birth"].strftime(
            "%Y-%m-%d"
        )

    async def test_delete_customer_successful(
        self, mock_customer_service, client, mock_customer_response
    ):
        """Tests happy path of DELETE /customers/{guid}."""

        test_customer_guid = "6d602a0c-f29d-4e44-8339-7642ccd07c5f"

        updated_resp_attrs = {
            "success": "true",
            "message": "Customer record deleted",
            "data": [],
        }

        for key, value in updated_resp_attrs.items():
            setattr(mock_customer_response, key, value)

        mock_customer_service.delete.return_value = mock_customer_response

        response = await client.delete(f"/customers/{test_customer_guid}")

        assert response.status_code == 200

        response_json = response.json()
        for field in updated_resp_attrs.keys():
            assert response_json[field] == updated_resp_attrs[field]
