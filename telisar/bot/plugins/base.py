import logging
import os
from textwrap import dedent
from importlib import import_module


class Plugin():
    """
    Define the interface for bot plugins.
    """
    command = None
    help_text = None

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        if not self.check_config():
            self.logger.error(f"Config check failed; disabling {self.__class__.__name__} plugin.")

    def run(self, message):
        """
        The main interface for plugins. Return values will be sent as a response to received commands.

        Your plugin may return either a string, a list of strings, or a generator yielding strings.
        """
        raise NotImplementedError()

    def check_config(self):
        """
        Called when your plugin is initialized; if it returns False, the plugin will be disabled.
        """
        return True


class PluginManager(Plugin):
    """
    This class is responsible for routing messages to plugins.
    """
    command = 'help'
    help_string = 'This message.'

    def __init__(self):
        self._command_map = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.WARNING)

    @property
    def command_map(self):
        return self._command_map

    def load_plugins(self):
        """
        Load plugins at runtime according to what's enabled in the dot env.
        """
        for plugin_name in os.getenv('DISCORD_BOT_PLUGINS', '').split(','):
            if plugin_name:
                import_module(f'telisar.bot.plugins.{plugin_name}')

        # always load the help plugin, and pass it a reference to our command map
        self._command_map['help'] = Help(self._command_map)

        # Now that we've loaded all plugin modules, register Help classes
        for plugin in Plugin.__subclasses__():
            self.logger.debug(f'Loading {plugin}')
            if plugin.command == 'help':
                continue
            self._command_map[plugin.command] = plugin()

    def get_plugin(self, message):
        """
        Message routing for plugin commands.
        """
        (cmd, parts) = message_parts(message)
        try:
            return self.command_map[cmd]
        except KeyError:
            pass


class Help(Plugin):
    """
    Useful commands for the Noobhammer! D&D Campaign.

    help............This message.
    help PLUGIN.....Display help for PLUGIN.

    """
    command = 'help'
    help_string = "This message."

    def __init__(self, command_map):
        super().__init__()
        self._command_map = command_map

    def _command_help(self, cmd):
        for plugin in self._command_map.values():
            if plugin.command == cmd:
                return self._command_map[cmd].__doc__
        return None

    @property
    def command_list(self):
        lines = []
        for plugin in self._command_map.values():
            lines.append(f'{plugin.command}: {plugin.help_string}')
        return '\n'.join(lines)

    def run(self, message):
        """
        Print the help documentation for the bot, or a specific ccommand.
        """
        helptext = ''
        try:
            (cmd, args) = message_parts(message)
            return self._command_help(args[0])
        except (IndexError, KeyError):
            pass

        if not helptext:
            return dedent(self.__doc__) + f"Available Plugins:\n{self.command_list}"


def message_parts(message):
    """
    Parse a Discord message object's content and return a tuple of the command and a list of arguments.
    """
    parts = message.content.split()
    return (parts[0][1:], parts[1:])
