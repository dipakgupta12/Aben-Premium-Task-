from this import d
import pytest
from network_failure_point import identify_router


@pytest.mark.parametrize(
    "graph, output",
    [
        ("1 -> 2 -> 3 -> 5 -> 2 -> 1", "2"),
        ("1 -> 3 -> 5 -> 6 -> 4 -> 5 -> 2 -> 6", "5"),
        ("2 -> 4 -> 6 -> 2 -> 5 -> 6", "2, 6"),
    ],
)
def test_network_failure_point(graph, output):
    assert identify_router(graph) == output


@pytest.mark.parametrize("graph, output", [
    ("2 -> 4 -> 6 -> 2 -> 5 -> 6", "2")
    ])
def test_failed(graph, output):
    assert identify_router(graph) != output
