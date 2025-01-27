from typing import List

from pydantic import ConfigDict

from src.schemas.account.account_base import AccountBase
from src.schemas.common import CommonRestModelConfig
from src.schemas.customer.customer_base import CustomerBase


class AccountOutput(AccountBase):
    """
    Rest Model for the Account Output Data Transfer Object (DTO).

    Used to return data to client.
    """

    customers: List[CustomerBase] = []

    model_config = ConfigDict(**CommonRestModelConfig.__dict__, title="AccountOutput")
