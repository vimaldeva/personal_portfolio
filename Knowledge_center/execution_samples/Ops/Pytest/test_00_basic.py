# import pytest 

def increment_5(x):
    return x+5

def test_increment_5():
    assert increment_5(10) == 15
    assert increment_5(-5) == 0
    

def test_increment_5_1():
    assert increment_5(0) == 5