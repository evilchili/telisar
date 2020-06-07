import pytest
import discord.client
from collections import namedtuple
from unittest.mock import MagicMock


mock_message = namedtuple('MockMessage', 'content')


@pytest.fixture
def mock_discord_user():
    return discord.user.ClientUser(state=MagicMock(), data=dict(
        id=1,
        username='test_hammer',
        discriminator='0',
        avatar=None,
    ))


@pytest.fixture
def mock_discord_guilds():
    return {
        1: discord.guild.Guild(
            data=dict(
                id=1,
                member_count=10,
                name='test_guild_1',
                region='test_region'
            ), state=MagicMock(),
        ),
        2: discord.guild.Guild(
            data=dict(
                id=2,
                member_count=10,
                name='test_guild_2',
                region='test_region'
            ), state=MagicMock(),
        ),
    }


def msg_factory(content):
    return mock_message(content=content)
