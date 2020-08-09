import logging
import pytest

from telisar.languages.elven import Elven, ElvenPerson, ElvenPlaceName


@pytest.fixture
def elven():
    e = Elven()
    e._logger.setLevel(logging.DEBUG)
    return e


@pytest.fixture
def person():
    e = ElvenPerson()
    e._logger.setLevel(logging.DEBUG)
    return e


@pytest.fixture
def place():
    e = ElvenPlaceName()
    e._logger.setLevel(logging.DEBUG)
    return e


@pytest.mark.parametrize('name', [
    'Ara am Akiir',
    'Elstuvian am Vakarilithien',
    'Lorithliani um Eleth',
    'Orinanthi',
    'Zandilar',
    'Rillifane Rallathil',
    'Labelas Enoreth',
    'Corellon Larethian',
    'Vandria Gilmadrith',
])
def test_existing_names(person, name):
    assert person.is_valid(name)


@pytest.mark.parametrize('name', [
    'el Vakar',
    'el Qatra',
    'el Astrum',
])
def test_existing_place_names(place, name):
    assert place.is_valid(name)


@pytest.mark.parametrize('name', [
    'Danta Kosht',
    'Bartok Brescht'
])
def test_invalid_names(person, name):
    assert not person.is_valid(name)

