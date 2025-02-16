from enum import Enum

from src.utils.retrieve_enum_values import get_enum_values


class RandomEnum(str, Enum):
    """Random enum used for testing."""

    FIRST_VALUE = 'first_value'
    SECOND_VALUE = 'second_value'
    THIRD_VALUE = 'third_value'


def test_get_enum_values():
    """Tests that get_enum_values returns the list of values in the enum."""
    expected_output = ["first_value", "second_value", "third_value"]

    actual_output = get_enum_values(RandomEnum)

    assert actual_output == expected_output
