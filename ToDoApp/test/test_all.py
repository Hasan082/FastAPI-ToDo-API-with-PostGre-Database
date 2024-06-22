import pytest


def testFn():
    assert 3 == 3
    assert 2 == 2


def deftestinstance():
    assert isinstance("this is str", str)


def test_boleean():
    validate = True
    assert validate is True
    assert ("world" is not int)


def test_gerate_tan_there():
    assert 7 > 3


def test_list():
    mulist = [1, 2, 3]
    anylist = [False, False]
    assert 1 in mulist
    assert 2 in mulist
    assert 3 in mulist
    assert all(mulist)
    assert not any(anylist)


class Student:
    def __init__(self, name, age, year):
        self.name = name
        self.age = age
        self.year = year


def default_employee():
    return Student("John", 25, 1999)


@pytest.fixture
def test_student(default_employee):
    assert default_employee.name == "John", 'First name should be John'
    assert default_employee.age == 24, 'Age should be 24'
    assert default_employee.year == 1999, 'Year should be 1999'
