from typing import Optional

from pydantic import BaseModel

from src.enums.account_status import AccountStatus


class AccountUpdate(BaseModel):
    """
    Rest Model for the Account Update Data Transfer Object (DTO).

    Used to serialise data sent in request for updating account records.
    """
    account_name: Optional[str] = None
    status: Optional[AccountStatus] = None
