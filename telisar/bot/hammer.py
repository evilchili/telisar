import os
import logging

import discord

from telisar.bot.plugins.base import PluginManager


class Hammer(discord.Client):
    """
    Discord bot for the Noobhammer Chronicles campaign.
    """
    def __init__(self):
        """
        Ye Olde Constructor. Initializes logging and plugins.
        """
        super().__init__()
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('websockets.protocol').setLevel(logging.ERROR)
        self._initialize_env()
        self._initialize_plugins()

    def _initialize_env(self):
        """
        initialize the bot parameters from the dot env.
        """
        self._token = os.getenv('DISCORD_TOKEN')
        self._command_prefix = os.getenv('DISCORD_COMMAND_PREFIX', '.')

    def _initialize_plugins(self):
        """
        Instantiate the plugin manager and load enabled plugins
        """
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()

    def run(self):
        """
        Connect to discord using the Discord client library and our token.
        """
        super().run(self._token)

    async def on_ready(self):
        logging.debug(f'Bot "{self.user}" has connected to Discord on guild "{self.guilds[0]}".')

    async def on_message(self, message):
        """
        Message routing.
        """

        #  Ignore anything that isn't addressed to us
        if message.content[0] != self._command_prefix:
            logging.debug(f'Message "{message.content[:10]}..." does not begin with bot command prefix '
                          '"{self._command_prefix}"; ignoring.')
            return

        #  Ignore our own messaging
        if message.author == self.user:
            logging.debug(f'Message "{message.content[:10]}..." originated with me; ignoring.')
            return

        #  If no plugin can handle the message, ignore it.
        plugin = self.plugin_manager.get_plugin(message)
        if not plugin:
            return

        # process the message using a plugin. If the plugin generates a response, send it.
        response = plugin.run(message)
        if response:
            await message.channel.send(response)
