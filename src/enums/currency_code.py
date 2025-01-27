from enum import Enum

class CurrencyCode(str, Enum):
    """
    Enumeration for currency code. This may be moved to a database table in the future.
    """
    EUR = "EUR"
    GBP = "GBP"
    USD = "USD"
