from typing import List, Optional, TypeVar

from pydantic.main import BaseModel

T = TypeVar("T")


class GenericResponseModel(BaseModel):
    """Base response model for all responses"""

    success: str
    message: Optional[str] = None
    data: List[T]
    status_code: Optional[int] = None
