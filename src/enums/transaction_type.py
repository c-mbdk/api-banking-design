from enum import Enum


class TransactionType(str, Enum):
    """
    Enumeration for the categorisation of the transaction.
    """

    CREDIT = "Credit"
    DEBIT = "Debit"
