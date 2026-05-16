import pytest


@pytest.fixture
def setup():
    print("Launch Browser")
    print("Login to Application")
    print("Browse products")

    yield 
    print("Logoff")
    print("Close Browser")

def test_add_to_cart(setup):
    print("Add item successful")

def test_remove_from_cart(setup):
    print("Remove item successful")


