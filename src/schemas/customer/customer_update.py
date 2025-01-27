from typing import Optional

from pydantic import BaseModel


class CustomerUpdate(BaseModel):
    """
    Rest Model for the Customer Update Data Transfer Object (DTO).

    Used to serialise data sent in request for updating customer records.
    """

    first_name: Optional[str] = None
    middle_names: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email_address: Optional[str] = None
    address: Optional[str] = None
