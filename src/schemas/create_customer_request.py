from datetime import date
from typing import Annotated, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from src.enums.account_status import AccountStatus
from src.schemas.common import CommonRestModelConfig
from src.utils.constants import EXAMPLE_GUID_1
from src.utils.regex_patterns import NAME_PATTERN, UUID4_PATTERN


class CreateCustomerRequest(BaseModel):
    """
    Rest Model for the Create Customer Request Data Transfer Object (DTO).

    Used to serialise data from the client request to create customer
    records.
    """

    customer_guid: Annotated[
        str, StringConstraints(pattern=UUID4_PATTERN, strict=True)
    ] = Field(
        default=uuid4(),
        description="Unique identifier for the customer record.",
        examples=[EXAMPLE_GUID_1],
        json_schema_extra={"pattern": UUID4_PATTERN},
    )
    first_name: Annotated[str, StringConstraints(pattern=NAME_PATTERN, strict=True)] = (
        Field(
            ...,
            description="First name of the customer.",
            examples=["Jane"],
        )
    )
    middle_names: Annotated[
        Optional[str], StringConstraints(pattern=NAME_PATTERN, strict=True)
    ] = Field(
        default=None,
        description="Middle names of the customer.",
        examples=["Geoffrey"],
    )
    last_name: Annotated[str, StringConstraints(pattern=NAME_PATTERN, strict=True)] = (
        Field(
            ...,
            description="Last name (surname) of the customer",
            examples=["Doe", "Bloggs"],
        )
    )
    date_of_birth: date = Field(
        ...,
        description="Customer's birthdate",
        examples=["1997-08-21"],
    )
    phone_number: str = Field(
        default=None,
        description="Customer's phone number",
        examples=["07123456789"],
    )
    email_address: str = Field(
        default=None,
        description="Customer's email address",
        examples=["joe.bloggs@gmails.com"],
    )
    address: str = Field(
        ...,
        description="Customer's primary address",
        examples=["123 Baker Street, London, E12 345"],
    )
    account_guid: Annotated[
        str, StringConstraints(pattern=UUID4_PATTERN, strict=True)
    ] = Field(
        default=uuid4(),
        description="Unique identifier for the account.",
        examples=[EXAMPLE_GUID_1],
        pattern=UUID4_PATTERN,
    )
    account_name: str = Field(
        default={},
        description="Name of the account",
        examples=["Jean's Current Account"],
    )
    account_status: AccountStatus = Field(
        default=AccountStatus.ACTIVE,
        description="Status of the account.",
        examples=[AccountStatus.ACTIVE],
    )

    model_config = ConfigDict(
        **CommonRestModelConfig.__dict__, title="CreateCustomerRequest"
    )
