import logging
import pytest
from telisar.languages.common import Common, CommonPerson


@pytest.fixture
def common():
    e = CommonPerson()
    e._logger.setLevel(logging.DEBUG)
    return e


@pytest.mark.parametrize('name', [
    'Banu',
    'Tak',
    'William Johnson MacDougal',
    'Kris',
    'Randal',
    'Belia',
    'Met',
    'Adi',
    'Migas',
])
def test_existing_names(common, name):
    assert common.is_valid(name)
