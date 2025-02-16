from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from src.enums.account_status import AccountStatus
from src.schemas.common import CommonRestModelConfig
from src.utils.constants import EXAMPLE_GUID_1, EXAMPLE_GUID_2
from src.utils.regex_patterns import UUID4_PATTERN


class AccountBase(BaseModel):
    """
    Base for Account Data Transfer Objects (DTOs).
    """

    guid: Annotated[str, StringConstraints(pattern=UUID4_PATTERN, strict=True)] = Field(
        description="Unique identifier for the account.",
        examples=[EXAMPLE_GUID_1],
        pattern=UUID4_PATTERN,
    )
    account_name: str = Field(
        ..., description="Name on the account", examples=["Doe FlexAccount"]
    )
    status: AccountStatus = Field(
        ..., description="Status of the account", examples=["ACTIVE", "INACTIVE"]
    )

    model_config = ConfigDict(**CommonRestModelConfig.__dict__, title="AccountBase")
