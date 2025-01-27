from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI, HTTPException
from httpx import ASGITransport, AsyncClient

from src.api.v1.routers.account import router
from src.schemas.base_response import GenericResponseModel
from src.services.account_service import AccountService, get_account_service
from tests.shared.constants import test_url


class TestAccountRouter:
    """Test suite for /accounts route."""

    @pytest.fixture
    def mock_account_service(self):
        """Provides mock account service instance for testing."""
        mock_service = AsyncMock(spec=AccountService)

        return mock_service

    @pytest.fixture
    def mock_account_response(self, mock_account_customer_base):
        """Provides base mock response for AccountService."""
        return GenericResponseModel(
            success="true",
            message="Available account data returned",
            status_code=200,
            data=[mock_account_customer_base.model_dump()],
        )

    @pytest.fixture(scope="function")
    def test_app(self, mock_account_service):
        """
        Fixture for app configured with mock account service.
        """
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_account_service] = lambda: mock_account_service

        return app

    @pytest.fixture(scope="function")
    async def client(self, test_app):
        """Fixture for test client."""
        async with AsyncClient(
            transport=ASGITransport(test_app), base_url=test_url
        ) as client:
            yield client

    async def test_get_accounts_success(
        self,
        mock_account_service,
        client,
        mock_account_response,
        mock_account_customer_base,
    ):
        """Tests happy path for GET /accounts."""

        mock_account_service.get_all.return_value = mock_account_response

        response = await client.get("/accounts")

        assert response.status_code == 200

        response_json = response.json()
        for field in ["success", "status_code", "message"]:
            assert response_json[field] == getattr(mock_account_response, field)

        # Assert against account records returned in data attribute
        resp_data_field_list = list(mock_account_response.data[0].keys())
        resp_data_field_list.remove("customers")
        for field in resp_data_field_list:
            assert (
                response_json["data"][0][field] == mock_account_response.data[0][field]
            )  # noqa

        customer_field_list = list(mock_account_response.data[0]["customers"][0].keys())
        customer_field_list.remove("date_of_birth")

        for field in customer_field_list:
            assert response_json["data"][0]["customers"][0][field] == getattr(
                mock_account_customer_base.customers[0], field
            )  # noqa

        assert response_json["data"][0]["customers"][0][
            "date_of_birth"
        ] == mock_account_response.data[0]["customers"][0]["date_of_birth"].strftime(
            "%Y-%m-%d"
        )  # noqa

    async def test_get_single_account_success(
        self, mock_account_service, client, mock_account_response
    ):
        """Tests happy path of GET /accounts/{guid}"""

        test_account_guid = "af7ac985-9d0f-4c98-9605-cee7bcc64554"

        mock_account_response.data[0]["guid"] = test_account_guid

        test_account_data = {
            "guid": test_account_guid,
            "account_name": "Current Account - John Doe",
        }

        for key, value in test_account_data.items():
            mock_account_response.data[0][key] = value

        test_customer_data = {
            "guid": "8afbe3a3-874c-4c8a-a0d5-5f65c8b83b53",
            "first_name": "Jillian",
            "middle_names": "Angela",
            "last_name": "Doe",
            "date_of_birth": "1995-08-31",
            "email_address": "jillian.a.doe@email.com",
            "phone_number": "07123989796",
            "address": "94 Sesame Street, London, S12 P89",
        }

        for key, value in test_customer_data.items():
            mock_account_response.data[0][key] = value

        mock_account_service.get_account.return_value = mock_account_response

        response = await client.get(f"/accounts/{test_account_guid}")

        assert response.status_code == 200

        response_json = response.json()
        for field in ["success", "status_code", "message"]:
            assert response_json[field] == getattr(mock_account_response, field)

        # Assert against account records returned in data attribute
        resp_data_field_list = list(mock_account_response.data[0].keys())
        resp_data_field_list.remove("customers")
        for field in resp_data_field_list:
            assert (
                response_json["data"][0][field] == mock_account_response.data[0][field]
            )  # noqa

        customer_field_list = list(test_customer_data.keys())
        customer_field_list.remove("date_of_birth")

        for field in customer_field_list:
            assert (
                response_json["data"][0]["customers"][0][field]
                == mock_account_response.data[0]["customers"][0][field]
            )  # noqa

        assert response_json["data"][0]["customers"][0][
            "date_of_birth"
        ] == mock_account_response.data[0]["customers"][0]["date_of_birth"].strftime(
            "%Y-%m-%d"
        )  # noqa

    async def test_get_single_account_failure(
        self,
        mock_account_service,
        client,
    ):
        """Tests unhappy path of GET /accounts/{guid}."""
        test_account_guid = "b9d43e4d-788e-463f-a415-eb52b105c560"

        mock_account_service.get_account.side_effect = HTTPException(
            status_code=404, detail=f"Account not found: {test_account_guid}"
        )

        response = await client.get(f"/accounts/{test_account_guid}")

        assert response.status_code == 404
        assert response.json() == {"detail": f"Account not found: {test_account_guid}"}

    async def test_update_account_successful(
        self, mock_account_service, client, mock_account_response
    ):
        """Tests happy path of PUT /accounts/{guid}."""

        test_account_guid = "2c94ad22-2c67-47b9-a88e-55abcd63ecdf"

        updated_account_data = {"account_name": "Current Account - Jonathan"}

        mock_account_response.data[0]["account_name"] = updated_account_data[
            "account_name"
        ]  # noqa

        mock_account_service.update.return_value = mock_account_response

        response = await client.put(
            f"/accounts/{test_account_guid}",
            json=updated_account_data,
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200

        response_json = response.json()
        for field in ["success", "status_code", "message"]:
            assert response_json[field] == getattr(mock_account_response, field)

        # Assert against account records returned in data attribute
        resp_data_field_list = list(mock_account_response.data[0].keys())
        resp_data_field_list.remove("customers")
        for field in resp_data_field_list:
            assert (
                response_json["data"][0][field] == mock_account_response.data[0][field]
            )  # noqa

        customer_field_list = list(mock_account_response.data[0]["customers"][0].keys())
        customer_field_list.remove("date_of_birth")

        for field in customer_field_list:
            assert (
                response_json["data"][0]["customers"][0][field]
                == mock_account_response.data[0]["customers"][0][field]
            )  # noqa

        assert response_json["data"][0]["customers"][0][
            "date_of_birth"
        ] == mock_account_response.data[0]["customers"][0]["date_of_birth"].strftime(
            "%Y-%m-%d"
        )  # noqa

    async def test_delete_account_successful(
        self, mock_account_service, client, mock_account_response
    ):
        """Tests happy path of DELETE /accounts/{guid}."""

        test_account_guid = "817cf924-105c-47e3-8ac3-e4e620a4f996"

        updated_resp_attrs = {
            "success": "true",
            "message": "Account record deleted",
            "data": [],
        }

        for key, value in updated_resp_attrs.items():
            setattr(mock_account_response, key, value)

        mock_account_service.delete.return_value = mock_account_response

        response = await client.delete(f"/accounts/{test_account_guid}")

        assert response.status_code == 200

        response_json = response.json()
        for field in updated_resp_attrs.keys():
            assert response_json[field] == updated_resp_attrs[field]
