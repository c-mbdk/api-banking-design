import json

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.api.v1.routers.customer import router
from tests.shared.constants import test_url


class TestCustomerRouter:
    """Integration test suite for the customer router."""

    @pytest.fixture(scope="function")
    def test_app(self):
        """Fixture for app configured with db."""
        app = FastAPI()
        app.include_router(router)
        return app

    @pytest.fixture(scope="function")
    async def client(self, test_app):
        async with AsyncClient(
            transport=ASGITransport(test_app), base_url=test_url
        ) as client:
            yield client

    async def test_post_customer_returns_200(
        self,
        client,
        valid_input_customer_account_data,
        valid_customer_data_two,
        valid_account_data,
    ):
        """Tests happy path of POST /customers."""

        response = await client.post(
            "/customers",
            json=valid_input_customer_account_data,
        )

        expected_resp_attrs = {
            "status_code": 201,
            "message": "Customer record created",
            "success": "true",
        }

        assert response.status_code == 201

        response_json = response.json()

        for field in expected_resp_attrs.keys():
            assert response_json[field] == expected_resp_attrs[field]

        # Assert against customer records returned in data attribute
        resp_data_field_list = list(valid_customer_data_two[0].keys())
        response_customer_data = json.loads(response_json["data"][0])
        for field in resp_data_field_list:
            assert response_customer_data[field] == valid_customer_data_two[0][field]

        assert (
            response_customer_data["date_of_birth"]
            == valid_customer_data_two[0]["date_of_birth"]
        )

        for field in valid_account_data.keys():
            assert (
                response_customer_data["accounts"][0][field]
                == valid_account_data[field]
            )

    async def test_get_single_customer_returns_200(
        self,
        client,
        seed_db_customer_account,
        valid_customer_data_two,
        valid_account_data,
    ):
        """Tests happy path of GET /customers/{guid}."""

        customer_guid = valid_customer_data_two[0]["guid"]

        response = await client.get(f"/customers/{customer_guid}")

        assert response.status_code == 200

        response_json = response.json()

        expected_resp_attrs = {
            "status_code": 200,
            "message": "Available customer data returned",
            "success": "true",
        }

        for field in expected_resp_attrs.keys():
            assert response_json[field] == expected_resp_attrs[field]

        # Assert against customer records returned in data attribute
        resp_data_field_list = list(valid_customer_data_two[0].keys())
        response_customer_data = json.loads(response_json["data"][0])
        for field in resp_data_field_list:
            assert response_customer_data[field] == valid_customer_data_two[0][field]

        assert (
            response_customer_data["date_of_birth"]
            == valid_customer_data_two[0]["date_of_birth"]
        )

        for field in valid_account_data.keys():
            assert (
                response_customer_data["accounts"][0][field]
                == valid_account_data[field]
            )

    async def test_get_all_customers_returns_200(
        self,
        seed_db_customer_account,
        client,
        valid_account_data,
        valid_customer_data_two,
    ):
        """Tests happy path of GET /customers."""

        response = await client.get("/customers")

        assert response.status_code == 200

        response_json = response.json()

        expected_resp_attrs = {
            "status_code": 200,
            "message": "Available customer data returned",
            "success": "true",
        }

        for field in expected_resp_attrs.keys():
            assert response_json[field] == expected_resp_attrs[field]

        # Assert against customer records returned in data attribute
        resp_data_field_list = list(valid_customer_data_two[0].keys())
        response_customer_data = json.loads(response_json["data"][0])
        for field in resp_data_field_list:
            assert response_customer_data[field] == valid_customer_data_two[0][field]

        assert (
            response_customer_data["date_of_birth"]
            == valid_customer_data_two[0]["date_of_birth"]
        )

        for field in valid_account_data.keys():
            assert (
                response_customer_data["accounts"][0][field]
                == valid_account_data[field]
            )

    async def test_update_customer_returns_200(
        self,
        seed_db_customer_account,
        client,
        valid_account_data,
        valid_customer_data_two,
    ):
        """Tests happy path of PUT /customers/{guid}."""

        customer_guid = valid_customer_data_two[0]["guid"]

        updated_customer_data = {
            "first_name": "Joshua",
            "email_address": "joshua.bloggs@email.com",
        }

        for key, value in updated_customer_data.items():
            valid_customer_data_two[0][key] = value

        response = await client.put(
            f"/customers/{customer_guid}", json=updated_customer_data
        )

        assert response.status_code == 200

        response_json = response.json()

        expected_resp_attrs = {
            "status_code": 200,
            "message": "Customer record updated",
            "success": "true",
        }

        for field in expected_resp_attrs.keys():
            assert response_json[field] == expected_resp_attrs[field]

        # Assert against customer records returned in data attribute
        resp_data_field_list = list(valid_customer_data_two[0].keys())
        response_customer_data = json.loads(response_json["data"][0])
        for field in resp_data_field_list:
            assert response_customer_data[field] == valid_customer_data_two[0][field]

        assert (
            response_customer_data["date_of_birth"]
            == valid_customer_data_two[0]["date_of_birth"]
        )

        for field in valid_account_data.keys():
            assert (
                response_customer_data["accounts"][0][field]
                == valid_account_data[field]
            )

    async def test_delete_customer_returns_200(
        self,
        seed_db_customer_account,
        client,
        valid_customer_data_two,
    ):
        """Tests happy path of DELETE /customers/{guid}."""

        customer_guid = valid_customer_data_two[0]["guid"]

        response = await client.delete(f"/customers/{customer_guid}")

        assert response.status_code == 200

        response_json = response.json()

        expected_resp_attrs = {
            "status_code": 200,
            "success": "true",
            "message": "Customer record deleted",
            "data": [],
        }

        for field in expected_resp_attrs.keys():
            assert response_json[field] == expected_resp_attrs[field]

    async def test_post_customer_invalid_returns_422(
        self,
        valid_input_customer_account_data,
        client,
    ):
        """Tests unhappy path of POST /customers."""

        valid_input_customer_account_data["customer_guid"] = "123"

        response = await client.post(
            "/customers", json=valid_input_customer_account_data
        )

        assert response.status_code == 422
        response_json = response.json()

        assert f"String should match pattern" in response_json["detail"][0]["msg"]

    async def test_get_single_customer_invalid_guid_returns_404(
        self, valid_customer_data_two, client, seed_db_customer_account
    ):
        """Tests unhappy path of GET /customers/{guid}."""

        customer_guid = "4aef59c6-9dbd-46ec-b111-88e0ffdb0314"

        response = await client.get(f"/customers/{customer_guid}")

        assert response.status_code == 404

        response_json = response.json()

        assert response_json["detail"] == f"Customer not found: {customer_guid}"

    async def test_update_customer_invalid_data_returns_404(
        self, valid_customer_data_two, client, seed_db_customer_account
    ):
        """Tests unhappy path of PUT /customers/{guid}."""

        test_guid = "fbeda53a-e153-4ece-8ebb-0b4d6b93e130"

        updated_customer_data = {
            "first_name": "Jimm)",
            "email_address": "jimmy.bloggs@email.com",
        }

        response = await client.put(
            f"/customers/{test_guid}", json=updated_customer_data
        )

        assert response.status_code == 422
        response_json = response.json()

        assert "String should match pattern" in response_json["detail"][0]["msg"]

    async def test_delete_customer_invalid_guid_returns_404(
        self, valid_customer_data_two, client, seed_db_customer_account
    ):
        """Tests unhappy path of DELETE /customers/{guid}."""

        test_guid = "fbeda53a-e153-4ece-8ebb-0b4d6b93e130"

        response = await client.delete(f"/customers/{test_guid}")

        assert response.status_code == 404
        response_json = response.json()

        assert response_json["detail"] == f"Customer not found: {test_guid}"
