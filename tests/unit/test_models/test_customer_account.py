from src.models.banking_models import Account, Customer


def test_valid_customer_created_with_account(valid_account_data, valid_customer_data):
    """Tests that customer and account records can be linked."""

    new_customer = Customer(**valid_customer_data)

    account_data = valid_account_data.copy()
    account_data["customers"] = [new_customer]

    new_account = Account(**account_data)

    field_list = list(account_data.keys())
    field_list.remove("customers")

    for field in field_list:
        assert getattr(new_account, field) == account_data[field]

    assert new_account.customers[0] == new_customer
