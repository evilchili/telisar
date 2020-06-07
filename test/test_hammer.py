import pytest
from conftest import msg_factory
from telisar.bot import hammer


@pytest.fixture
def bot(monkeypatch, mock_discord_guilds, mock_discord_user, event_loop):

    # configure the environment
    monkeypatch.setenv('DISCORD_TOKEN', 'test-token')
    monkeypatch.setenv('DISCORD_COMMAND_PREFIX', '.')

    # instantiate a bot with a mock user and guilds
    h = hammer.Hammer()
    h._connection.user = mock_discord_user
    h._connection._guilds = mock_discord_guilds
    return h


@pytest.mark.asyncio
async def test_on_ready(bot):
    await bot.on_ready()


@pytest.mark.asyncio
@pytest.mark.parametrize('message', [
    msg_factory('hello')
])
async def test_on_message(bot, message):
    await bot.on_message(message)
