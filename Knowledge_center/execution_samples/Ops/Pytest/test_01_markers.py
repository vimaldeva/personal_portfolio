import pytest


def increment_11(x):
    return x+11

@pytest.mark.vimal
def test_increment_5():
    assert increment_11(10) == 21
    assert increment_11(-5) == 6

