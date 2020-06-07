import random

import pytest

from telisar.bot.plugins import roll
from conftest import msg_factory


@pytest.fixture
def plugin():
    return roll.Roll()


@pytest.mark.parametrize('message', [
    msg_factory('.roll 0d0'),
    msg_factory('.roll 0d1'),
    msg_factory('.roll 1d0'),
    msg_factory('.roll -3d'),
    msg_factory('.roll 3d'),
    msg_factory('.roll 3d-10'),
    msg_factory('.roll 1d101'),
    msg_factory('.roll 101d1'),
])
def test_roll_invalid_input(plugin, message):
    assert "Invalid" in plugin.run(message)


def test_roll(plugin):

    def _randint():
        return random.randint(1, 100)

    testcase = f"roll {_randint()}d{_randint()}"
    assert "Invalid" not in plugin.run(msg_factory(testcase))
