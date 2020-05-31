from telisar.bot.plugins.base import Plugin


class Echo(Plugin):

    command = 'echo'
    help_string = "Test bot communications."

    def run(self, message):
        response = f'{message.author} said, "{message.content}"'
        return response
