from enum import Enum


class AccountStatus(str, Enum):
    """
    Enumeration for (bank) account status.
    """

    ACTIVE = "Active"
    INACTIVE = "Inactive"
