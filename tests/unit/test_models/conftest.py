import pytest

from src.enums.account_status import AccountStatus
from tests.shared.constants import TEST_GUID_1, TEST_GUID_2

test_customer_guid = TEST_GUID_1
test_first_name = "Jolene"
test_middle_names = "Dolly"
test_last_name = "Doe"
test_phone_number = "01234567891"
test_email_address = "jolene.dolly.doe@gmails.com"
test_address = "123 Baker Street, London, E12 345"
test_account_guid = TEST_GUID_2
test_account_name = "TEST ACCOUNT 123"
test_account_status = AccountStatus.ACTIVE


@pytest.fixture
def valid_customer_data():
    """Fixture to provide valid customer data."""

    return {
        "guid": test_customer_guid,
        "first_name": test_first_name,
        "middle_names": test_middle_names,
        "last_name": test_last_name,
        "phone_number": test_phone_number,
        "email_address": test_email_address,
        "address": test_address,
    }


@pytest.fixture
def valid_account_data():
    """Fixture to provide valid account data."""

    return {
        "guid": test_account_guid,
        "account_name": test_account_name,
        "status": test_account_status,
    }
