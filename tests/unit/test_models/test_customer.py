from src.models.banking_models import Customer


def test_valid_customer(valid_customer_data):
    """Tests that valid customer data can be used to create a Customer instance."""
    new_customer = Customer(**valid_customer_data)

    for field in valid_customer_data.keys():
        assert getattr(new_customer, field) == valid_customer_data[field]
