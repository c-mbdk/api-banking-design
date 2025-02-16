from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints

from src.utils.regex_patterns import NAME_PATTERN


class CustomerUpdate(BaseModel):
    """
    Rest Model for the Customer Update Data Transfer Object (DTO).

    Used to serialise data sent in request for updating customer records.
    """

    first_name: Annotated[
        Optional[str], StringConstraints(pattern=NAME_PATTERN, strict=True)
    ] = None
    middle_names: Annotated[
        Optional[str], StringConstraints(pattern=NAME_PATTERN, strict=True)
    ] = None
    last_name: Annotated[
        Optional[str], StringConstraints(pattern=NAME_PATTERN, strict=True)
    ] = None
    phone_number: Optional[str] = None
    email_address: Optional[str] = None
    address: Optional[str] = None
