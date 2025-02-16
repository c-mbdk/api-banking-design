from src.models.banking_models import Account


def test_valid_account(valid_account_data):
    """Tests that valid account data can be used to create an Account instance."""

    new_account = Account(**valid_account_data)
    
    for field in valid_account_data.keys():
        assert getattr(new_account, field) == valid_account_data[field]
