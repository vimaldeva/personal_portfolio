import pytest

@pytest.mark.parametrize("a,b,expected", [(10, 5, 15), (-5, 5, 0), (0, 0, 0)])
def test_increment_5(a, b, expected):
    assert a + b == expected