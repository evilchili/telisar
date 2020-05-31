from telisar.bot.plugins.base import Plugin, message_parts
from telisar.reckoning import calendar


class Date(Plugin):

    command = 'date'
    help_string = "Telisaran calendar interface."

    def __init__(self):
        self.calendar = calendar.Calendar()

    def run(self, message):
        (_, parts) = message_parts(message)

        if not parts:
            cmd = 'today'
        else:
            cmd = parts[0]

        attr = getattr(self.calendar, cmd)
        try:
            return getattr(attr, parts[1])
        except AttributeError:
            try:
                return attr(parts[1:])
            except TypeError:
                return repr(attr)
