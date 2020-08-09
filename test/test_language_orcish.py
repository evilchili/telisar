import logging
import pytest
from telisar.languages.orcish import Orcish, HalfOrcPerson


@pytest.fixture
def orcish():
    e = Orcish()
    e._logger.setLevel(logging.DEBUG)
    return e


@pytest.fixture
def halforc_person():
    e = HalfOrcPerson()
    e._logger.setLevel(logging.DEBUG)
    return e


@pytest.mark.parametrize('name', [
    'Ara am Akiir',
    'Zandilar',
])
def test_invalid_names(halforc_person, name):
    assert not halforc_person.is_valid(name)


@pytest.mark.parametrize('name', [
    'Danta Kosht',
    'Bartok Brescht',
])
def test_existing_names(halforc_person, name):
    assert halforc_person.is_valid(name)
