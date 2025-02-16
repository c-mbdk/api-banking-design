import json

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
import pytest

from src.api.v1.routers.account import router
from tests.shared.constants import test_url


class TestAccountRouter:
    """Integration test suite for the account router."""
    
    @pytest.fixture(scope="function")
    def test_app(self):
        """Fixture for app configured with db."""
        app = FastAPI()
        app.include_router(router)
        return app
    
    @pytest.fixture(scope="function")
    async def client(self, test_app):
        """Fixture for test client."""
        async with AsyncClient(
            transport=ASGITransport(test_app), base_url=test_url
        ) as client:
            yield client

    async def test_get_accounts_success_returns_200(
        self,
        seed_db_customer_account,
        client,
        valid_account_data,
        valid_customer_data_two,
    ):
        """Tests happy path for GET /accounts."""

        response = await client.get("accounts")

        assert response.status_code == 200
        
        response_json = response.json()

        expected_response = {
            "message": "Available account data returned",
            "success": "true",
            "status_code": 200
        }

        for field in expected_response.keys():
            assert response_json[field] == expected_response[field]

        response_account_data = json.loads(response_json["data"][0])
        for field in valid_account_data.keys():
            assert response_account_data[field] == valid_account_data[field]

        response_customer_data = response_account_data["customers"][0]
        for field in valid_customer_data_two[0].keys():
            assert response_customer_data[field] == valid_customer_data_two[0][field]

    async def test_get_account_success_returns_200(
        self,
        seed_db_customer_account,
        client,
        valid_account_data,
        valid_customer_data_two,
    ):
        """Tests happy path for GET /accounts/{guid}."""

        expected_account_guid = valid_account_data["guid"]
        response = await client.get(f"/accounts/{expected_account_guid}")

        assert response.status_code == 200
        
        response_json = response.json()

        expected_response = {
            "message": "Available account data returned",
            "success": "true",
            "status_code": 200
        }

        for field in expected_response.keys():
            assert response_json[field] == expected_response[field]

        assert len(response_json["data"]) == 1

        response_account_data = json.loads(response_json["data"][0])
        for field in valid_account_data.keys():
            assert response_account_data[field] == valid_account_data[field]

        response_customer_data = response_account_data["customers"][0]
        for field in valid_customer_data_two[0].keys():
            assert response_customer_data[field] == valid_customer_data_two[0][field]


    async def test_update_account_data_success_returns_200(
        self,
        valid_account_data,
        valid_customer_data_two,
        seed_db_customer_account,
        client
    ):
        """Tests happy path for PUT /accounts/{guid}."""

        account_guid = valid_account_data["guid"]
        updated_account_data = {
            "account_name": "New Account Name 1122"
        }
        valid_account_data["account_name"] = updated_account_data["account_name"]

        response = await client.put(
            f"/accounts/{account_guid}",
            json=updated_account_data,
        )

        assert response.status_code == 200

        response_json = response.json()

        response_account_data = json.loads(response_json["data"][0])
        for field in valid_account_data.keys():
            assert response_account_data[field] == valid_account_data[field]

        response_customer_data = response_account_data["customers"][0]
        for field in valid_customer_data_two[0].keys():
            assert response_customer_data[field] == valid_customer_data_two[0][field]


    async def test_delete_valid_account_returns_200(
        self,
        client,
        seed_db_customer_account,
        valid_account_data
    ):
        """Tests happy path of DELETE /accounts/{guid}."""

        account_guid = valid_account_data["guid"]

        response = await client.delete(f"/accounts/{account_guid}")

        expected_response = {
            "status_code": 200,
            "success": "true",
            "message": "Account record deleted",
            "data": []
        }

        assert response.status_code == 200

        response_json = response.json()

        for field in expected_response.keys():
            assert response_json[field] == expected_response[field]

    async def test_get_invalid_account_returns_404(
        self,
        client,
        seed_db_customer_account,
    ):
        """Tests unhappy path of GET /accounts/{guid}."""

        test_account_guid = "cc3e735e-4150-4600-bad5-ddf6986b51b1"

        response = await client.get(f"/accounts/{test_account_guid}")

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["detail"] == f"Account not found: {test_account_guid}"


    async def test_update_invalid_account_returns_404(
        self,
        client,
        seed_db_customer_account,
    ):
        """Tests unhappy path of PUT /accounts/{guid}."""

        test_account_guid = "e0196998-d220-46b3-9278-c17e23427c4c"

        updated_account_data = {
            "account_name": "New Account Name 9998"
        }

        response = await client.put(
            f"/accounts/{test_account_guid}",
            json=updated_account_data,
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["detail"] == f"Account not found: {test_account_guid}"


    async def test_delete_invalid_account_returns_404(
        self,
        client,
        seed_db_customer_account,
    ):
        """Tests unhappy path of DELETE /accounts/{guid}."""

        test_account_guid = "c52d26cc-db7e-498a-81b1-8aa0f9020b72"

        response = await client.delete(f"/accounts/{test_account_guid}")

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["detail"] == f"Account not found: {test_account_guid}"
