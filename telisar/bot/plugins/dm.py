import os

from telisar.bot.plugins.base import Plugin, message_parts

DM_USERNAME_VARIABLE = 'DM_USERNAME'


class DM(Plugin):
    """
    Tools for the DM.
    """
    command = 'dm'
    help_text = 'Tools for the DM.'

    def __init__(self):
        self._dm = None
        super().__init__()

    def check_config(self):
        self._dm = os.environ.get(DM_USERNAME_VARIABLE, None)
        if not self._dm:
            self.logger.error(f"{DM_USERNAME_VARIABLE} not defined.")
            return False
        return True

    def cmd_npc(race=None):
        """
        Return a randomly-generated NPC.
        """
        return "Not implemented yet."

    def run(self, message):
        """
        Message routing for DM commands. Ignores anyone not the DM.
        """

        if message.author != self._dm:
            return f"{message.author}: You are not the DM. Request denied."

        (_, (cmd, *args)) = message_parts(message)

        try:
            handler = getattr(self, f"cmd_{cmd.lower()}")
        except AttributeError:
            self.logger.debug(f"Ignoring unsupported command: {cmd}")
            return

        return handler(*args)
