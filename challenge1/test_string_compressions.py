import pytest
from string_compression import compress


@pytest.mark.parametrize(
    "string, output", [
        ("bbcceeee", "b2c2e4"),
        ("aaabbbcccaaa", "a3b3c3a3"),
        ("a", "a")
        ]
)
def test_string_compression(string, output):
    assert compress(string) == output
