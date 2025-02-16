from datetime import date
from typing import Annotated, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from src.schemas.common import CommonRestModelConfig
from src.utils.constants import EXAMPLE_GUID_1, EXAMPLE_GUID_2
from src.utils.regex_patterns import NAME_PATTERN, UUID4_PATTERN


class CustomerBase(BaseModel):
    """
    Base for the Customer Data Transfer Objects (DTOs).
    """

    guid: Annotated[str, StringConstraints(pattern=UUID4_PATTERN, strict=True)] = Field(
        default=uuid4(),
        description="Unique identifer for the customer record",
        strict=True,
        examples=[EXAMPLE_GUID_1, EXAMPLE_GUID_2],
        json_schema_extra={"pattern": UUID4_PATTERN},
    )
    first_name: Annotated[str, StringConstraints(pattern=NAME_PATTERN, strict=True)] = Field(
        ...,
        description="First name of the customer",
        examples=["Joe", "Jane"],
    )
    middle_names: Annotated[Optional[str], StringConstraints(pattern=NAME_PATTERN, strict=True)] = Field(
        default=None,
        description="Middle name of the customer",
        examples=["Andrew", "Anne"],
    )
    last_name: Annotated[str, StringConstraints(pattern=NAME_PATTERN, strict=True)] = Field(
        ...,
        description="Last name (surname) of the customer",
        examples=["Doe", "Bloggs"],
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

    model_config = ConfigDict(**CommonRestModelConfig.__dict__, title="CustomerBase")
