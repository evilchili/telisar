from telisar.bot.plugins import hoarding
from telisar import bag_of_hoarding
from conftest import msg_factory
import pytest


@pytest.fixture
def env(monkeypatch):
    monkeypatch.setenv(bag_of_hoarding.DATA_PATH_VARIABLE, 'data')


@pytest.fixture
def plugin(env):
    return hoarding.BagOfHoarding()


@pytest.mark.parametrize('message, expected_lines', [
    (".hoard", 1),
    (".hoard 5", 5),
])
def test_run(plugin, message, expected_lines):
    output = list(plugin.run(msg_factory(message)))
    print(output)
    assert len(output) == expected_lines


def test_HoardItem(env):
    assert bag_of_hoarding.HoardItem((bag_of_hoarding.DATA_PATH_VARIABLE))
