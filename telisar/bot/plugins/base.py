import pathlib
import logging
from importlib import import_module


class Plugin():
    command = None
    help_text = None

    def run(self, message):
        raise NotImplementedError()


class PluginManager(Plugin):
    command = 'help'
    help_string = 'This message.'

    def __init__(self):
        self._plugin_path = pathlib.Path(pathlib.Path(__file__).parent.absolute())
        self._command_map = {}
        self.logger = logging.getLogger('PluginManager')
        self.logger.setLevel(logging.WARNING)

    @property
    def command_map(self):
        return self._command_map

    def load_plugins(self):
        for fileobj in self._plugin_path.glob('*.py'):
            if fileobj.name in ('base.py', '__init__.py'):
                continue
            import_module(f'bot.plugins.{fileobj.name[:-3]}')

        self._command_map['help'] = self
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

    def run(self, message):
        helptext = []
        for plugin in self.command_map.values():
            helptext.append(f'{plugin.command}: {plugin.help_string}')
        return '\n'.join(helptext)


def message_parts(message):
    parts = message.content.split()
    return (parts[0][1:], parts[1:])
