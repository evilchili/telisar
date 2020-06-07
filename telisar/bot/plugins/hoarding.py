import os
import random
import dice
from functools import partial
from telisar.bot.plugins.base import Plugin, message_parts


class HoardItem:
    """
    A random item in Whisper's Bag of Hoarding.
    """
    def __init__(self, path):
        self._nouns = os.path.join(path, 'nouns')
        self._adjectives = os.path.join(path, 'adjectives')
        self._population_cache = {}

    @property
    def noun(self):
        """
        A random noun.
        """
        with open(self._nouns) as filehandle:
            line = self._random_line(filehandle).strip()
        return line.replace('_', ' ')

    @property
    def adjectives(self):
        """
        A string containing a comma-separated list of 1 or 2 random adjectives.
        """
        with open(self._adjectives) as filehandle:
            adj = []
            for i in range(random.choice([1, 2])):
                adj.append(self._random_line(filehandle).strip().replace('_', ' '))
        return ', '.join(adj)

    def _random_line(self, filehandle):
        """
        Choose a random line from a filehandle without loading the entire file into memory.
        """
        target = random.choice(range(self._line_count(filehandle)))
        filehandle.seek(0, 0)
        for line_number, line in enumerate(filehandle):
            if line_number == target:
                return line

    def _line_count(self, filehandle):
        """
        Count the number of lines in a file without having to hold the entire contents in memory.
        """
        if filehandle.name not in self._population_cache:
            filehandle.seek(0, 0)
            self._population_cache[filehandle.name] = \
                sum(chunk.count('\n') for chunk in iter(partial(filehandle.read, 1 << 15), ''))
        return self._population_cache[filehandle.name]

    def __str__(self):
        item = f"{self.adjectives} {self.noun}"
        if item[0] in 'aeiou':
            item = f"an {item}"
        else:
            item = f"a {item}"
        return item


class BagOfHoarding(Plugin):
    """
    Whisper's Bag of Hoarding

    hoard........Use Whisper's "Just What I Needed" action and try to pull a useful object from the Bag of Hoarding.
    hoard N......Pull N random items from the Bag of Hoarding.
    """
    command = 'hoard'
    help_string = "Pull a random item from Whisper's Bag of Hoarding"

    data_path_variable = 'HOARDING_DATA_PATH'

    def __init__(self):
        self._data_path = None
        super().__init__()

    def check_config(self):
        """
        Check the environment is properly configured.
        """
        self._data_path = os.environ.get(self.data_path_variable, None)
        if not self._data_path:
            self.logger.error(f"{self.data_path_variable} not defined.")
            return False
        return True

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
        for item in [HoardItem(self._data_path) for i in range(count)]:
            yield str(item)

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
