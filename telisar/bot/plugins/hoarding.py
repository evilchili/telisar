import dice
from telisar.bot.plugins.base import Plugin, message_parts
from telisar.bag_of_hoarding import HoardItem


class BagOfHoarding(Plugin):
    """
    Whisper's Bag of Hoarding

    hoard........Use Whisper's "Just What I Needed" action and try to pull a useful object from the Bag of Hoarding.
    hoard N......Pull N random items from the Bag of Hoarding.
    """
    command = 'hoard'
    help_text = "Pull a random item from Whisper's Bag of Hoarding"

    def __init__(self):
        self._data_path = None
        super().__init__()

    def cmd_hoard(self):
        """
        Pick one item from the Bag with a 75% chance of success. On failure, return a random item.
        """
        item = "just what you wanted"
        if dice.roll('1d4') == 1:
            item = HoardItem(self._data_path)
        yield f"You reach into your bag and retrieve... {item}!"

    def cmd_hoard_n(self, count=1):
        """
        Return a list of one or more random items from the Bag.
        """
        for i in range(count):
            yield HoardItem()

    def run(self, message):
        """
        Message routing for commands.
        """
        args = message_parts(message)[1]
        response = None

        # .hoard n
        try:
            count = int(args[0])
        except (IndexError, TypeError):
            pass
        else:
            response = self.cmd_hoard_n(count)

        # .hoard
        if not response:
            response = self.cmd_hoard()

        return response
