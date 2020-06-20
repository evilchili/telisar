import logging
import pytest

from telisar.languages.elven import Elven


@pytest.fixture
def elven():
    e = Elven()
    e._logger.setLevel(logging.DEBUG)
    return e


@pytest.mark.parametrize('name', [
    'Ara am Akiir',
    'Elstuvian am Vakarilithien',
])
def test_ara_am_akiir(elven, name):
    for n in name.split():
        assert elven.is_valid_word(n.lower())
