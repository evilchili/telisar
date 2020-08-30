from telisar.bot.plugins import search as search_plugin
from conftest import msg_factory
import pytest


@pytest.fixture
def env(monkeypatch):
    monkeypatch.setenv(search_plugin.DATA_PATH_VARIABLE, 'data')
    monkeypatch.setenv(search_plugin.SOURCE_PATH_VARIABLE, 'src')


@pytest.fixture
def plugin(env):
    return search_plugin.Search()


@pytest.mark.parametrize('message, expected_lines', [
    (".search foo", 1),
    (".search 5 foo", 1),
])
def test_run(plugin, message, expected_lines):
    output = list(plugin.run(msg_factory(message)))
    assert len(output) == expected_lines
