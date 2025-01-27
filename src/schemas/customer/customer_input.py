from typing import List

from pydantic import ConfigDict

from src.schemas.account.account_input import AccountInput
from src.schemas.common import CommonRestModelConfig
from src.schemas.customer.customer_base import CustomerBase


class CustomerInput(CustomerBase):
    """
    Rest Model for the Customer Input Data Transfer Object (DTO).

    Used to ensure valid customer data is saved in the db.
    """
    accounts: List[AccountInput] = [None]

    model_config = ConfigDict(**CommonRestModelConfig.__dict__, title="CustomerInput")
