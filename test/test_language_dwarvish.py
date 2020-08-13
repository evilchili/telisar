import logging
import pytest
from telisar.languages.dwarvish import Dwarvish


@pytest.fixture
def dwarvish():
    e = Dwarvish()
    e._logger.setLevel(logging.DEBUG)
    return e


@pytest.mark.parametrize('name', [
    'Moradin',
    'Ultar Ultarsson',
    'Julia Ultarsson',
])
def test_existing_names(dwarvish, name):
    assert dwarvish.is_valid(name)
