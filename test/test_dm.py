import pytest

from telisar.bot.plugins import dm
from conftest import msg_factory


@pytest.fixture
def plugin(monkeypatch):
    monkeypatch.setenv(dm.DM_USERNAME_VARIABLE, 'test')
    return dm.DM()


@pytest.mark.parametrize('msg, expected', [
    (msg_factory('.dm invalid command'), None),
    (msg_factory('.dm npc'), "Name"),
])
def test_run(msg, expected, plugin):
    assert plugin.run(msg) == expected
