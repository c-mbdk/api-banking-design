from enum import Enum
from typing import List


def get_enum_values(enum_class: Enum) -> List[str]:
    """
    Ensures Enum values will match the format expected by the database.
    Used in conjunction with the values_callable parameter for SQLAlchemy.

    Args:
        enum_class (Enum): The custom enum class.

    Returns:
        List[str]: The list of values in the specified enum class.
    """
    return [member.value for member in enum_class]
