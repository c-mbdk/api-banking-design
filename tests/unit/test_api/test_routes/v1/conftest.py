import pytest

from src.enums.account_status import AccountStatus
from src.schemas.account.account_output import AccountOutput
from src.schemas.customer.customer_output import CustomerOutput


@pytest.fixture
def mock_customer_account_base():
    """Provides base data for use in responses."""
    return CustomerOutput(
        guid="446d92d4-6497-4110-8278-bb4887993b6f",
        first_name="Josephine",
        middle_names="Anu",
        last_name="Doe",
        date_of_birth="1997-08-27",
        phone_number="07123898989",
        email_address="j.a.doe@email.com",
        address="64 Zoo Lane, London, W21 9GG",
        accounts=[
            AccountOutput(
                guid="c1248029-11b1-49d0-ab5f-4089f53b3d20",
                account_name="Current Account - Josephine",
                status=AccountStatus.ACTIVE,
            )
        ],
    )


@pytest.fixture
def mock_account_customer_base():
    """Provides base data for use in responses."""
    return AccountOutput(
        guid="6b39b1a9-27d9-47a6-bf61-85e110591df1",
        account_name="Current Account - Jake",
        status=AccountStatus.ACTIVE,
        customers=[
            CustomerOutput(
                guid="3dbc64b5-4235-46ae-be9d-53fd6e9a7efb",
                first_name="Jake",
                middle_names="Arthur",
                last_name="Doe",
                date_of_birth="1994-02-21",
                phone_number="07123767676",
                email_address="jake.a.doe@email.com",
                address="123 Narrow Street, Birmingham, B67 8DD",
            )
        ],
    )
