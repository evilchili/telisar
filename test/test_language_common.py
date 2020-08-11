import logging
import pytest
from telisar.languages.common import Common


@pytest.fixture
def common():
    e = Common()
    e._logger.setLevel(logging.DEBUG)
    return e


@pytest.mark.parametrize('name', [
    'Banu',
    'Tak',
    'William',
    'Kris',
    'Randal',
    'Belia',
    'Met',
    'Adi',
    'Migas',
])
def test_existing_names(common, name):
    assert common.is_valid(name)
