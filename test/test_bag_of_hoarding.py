from telisar.bot.plugins import hoarding
from conftest import msg_factory
import os
import pytest

@pytest.fixture
def env(monkeypatch):
    monkeypatch.setenv(hoarding.BagOfHoarding.data_path_variable, 'data')


@pytest.fixture
def plugin(monkeypatch, env):
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
    assert hoarding.HoardItem(os.environ.get(hoarding.BagOfHoarding.data_path_variable))
