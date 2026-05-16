import pytest


@pytest.fixture
def setup():
    print("Launch Browser")
    print("Login to Application")
    print("Browse products")

    yield 
    print("Logoff")
    print("Close Browser")