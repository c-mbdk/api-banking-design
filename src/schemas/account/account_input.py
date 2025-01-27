from pydantic import ConfigDict

from src.schemas.account.account_base import AccountBase
from src.schemas.common import CommonRestModelConfig


class AccountInput(AccountBase):
    """
    Rest Model for the Account Input Data Transfer Object (DTO).

    Used to ensure valid account data is saved in the db.
    """
    pass

    model_config = ConfigDict(**CommonRestModelConfig.__dict__, title="AccountInput")
