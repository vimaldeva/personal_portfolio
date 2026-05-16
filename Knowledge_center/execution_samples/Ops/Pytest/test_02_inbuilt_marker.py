import pytest


def increment_11(x):
    return x+11

@pytest.mark.skip(reason="This test is skipped because it is not relevant for the current testing phase.")
def test_increment_5():
    assert increment_11(10) == 21
    assert increment_11(-5) == 6

@pytest.mark.xfail(reason="This test is expected to fail because the function does not return the expected value.")
def test_increment_11():
    assert increment_11(10) == 20
