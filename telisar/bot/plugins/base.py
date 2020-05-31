import logging
import os
from importlib import import_module


class Plugin():
    """
    Define the interface for bot plugins.
    """
    command = None
    help_text = None

    def run(self, message):
        raise NotImplementedError()


class PluginManager(Plugin):
    """
    This class is responsible for routing messages to plugins.
    """
    command = 'help'
    help_string = 'This message.'

    def __init__(self):
        self._command_map = {}
        self.logger = logging.getLogger('PluginManager')
        self.logger.setLevel(logging.WARNING)

    @property
    def command_map(self):
        return self._command_map

    def load_plugins(self):
        """
        Load plugins at runtime according to what's enabled in the dot env.
        """
        for plugin_name in os.getenv('DISCORD_BOT_PLUGINS').split(','):
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
        (cmd, parts) = message_parts(message)
        try:
            return self.command_map[cmd]
        except KeyError:
            pass


class Help(Plugin):

    command = 'help'
    help_string = 'This message.'

    def __init__(self, command_map):
        super().__init__()
        self._command_map = command_map

    def run(self, message):
        helptext = []
        for plugin in self._command_map.values():
            helptext.append(f'{plugin.command}: {plugin.help_string}')
        return '\n'.join(helptext)


def message_parts(message):
    parts = message.content.split()
    return (parts[0][1:], parts[1:])
