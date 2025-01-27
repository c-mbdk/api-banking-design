from typing import List

from pydantic import ConfigDict

from src.schemas.account.account_output import AccountOutput
from src.schemas.common import CommonRestModelConfig
from src.schemas.customer.customer_base import CustomerBase


class CustomerOutput(CustomerBase):
    """
    Rest Model for the Customer Output Data Transfer Object (DTO).

    Used to return Customer data to client.
    """

    accounts: List[AccountOutput] = []

    model_config = ConfigDict(**CommonRestModelConfig.__dict__, title="CustomerOutput")
