from enum import Enum


class TransactionStatus(str, Enum):
    """
    Enumeration for the status of each transaction (in relation to payment completion).
    """

    COMPLETED = "Completed"
    PENDING = "Pending"
    DECLINED = "Declined"
    CANCELLED = "Cancelled"
