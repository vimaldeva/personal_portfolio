import pytest


@pytest.fixture(params=["a","b","c"])
def setup(request):
    print(request.param)

def test_login(setup):
    print("Login successful")
