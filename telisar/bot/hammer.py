import os
import logging

import discord

from telisar.bot.plugins.base import PluginManager


class Hammer(discord.Client):
    def __init__(self):
        super().__init__()
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('websockets.protocol').setLevel(logging.ERROR)
        self._initialize_env()
        self._initialize_plugins()

    def _initialize_env(self):
        self._token = os.getenv('DISCORD_TOKEN')
        self._command_prefix = os.getenv('COMMAND_PREFIX', '.')

    def _initialize_plugins(self):
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()

    def run(self):
        super().run(self._token)

    async def on_ready(self):
        logging.debug(f'Bot "{self.user}" has connected to Discord on guild "{self.guilds[0]}".')

    async def on_message(self, message, client):
        if message.content[0] != '.':
            logging.debug(f'Message "{message.content[:10]}..." does not begin with bot command prefix '
                          '"{self._command_prefix}"; ignoring.')
            return
        if message.author == client.user:
            logging.debug(f'Message "{message.content[:10]}..." originated with me; ignoring.')
            return

        plugin = self.plugin_manager.get_plugin(message)
        if not plugin:
            return

        response = plugin.run(message)
        if response:
            await message.channel.send(response)
