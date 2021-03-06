import os
import logging
import types

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
        logging.getLogger('discord.client').setLevel(logging.ERROR)
        logging.getLogger('discord.gateway').setLevel(logging.ERROR)
        logging.getLogger('discord.root').setLevel(logging.ERROR)
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

    async def send_response(self, message, response):
        if isinstance(response, types.GeneratorType) or isinstance(response, list):
            for res in response:
                if isinstance(res, str):
                    await message.channel.send(res)
                elif isinstance(res, discord.Embed):
                    await message.channel.send(embed=res)
        elif isinstance(response, discord.Embed):
            await message.channel.send(embed=response)
        else:
            await message.channel.send(response)

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
        try:
            response = None
            plugin = self.plugin_manager.get_plugin(message)
            logging.debug(f"Trying plugin {plugin}")
            if plugin:
                response = plugin.run(message)
                if not response:
                    return
            else:
                for plugin in self.plugin_manager.get_default_plugins():
                    logging.debug(f"Trying plugin {plugin}")
                    response = plugin.run(message)
                    if response:
                        break
            if response:
                await self.send_response(message, response)

        except Exception as e:
            logging.error("An error occurred executing the plugin.", exc_info=True)
            await message.channel.send(f"I AM ERROR: {e}")
