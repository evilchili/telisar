import random
import os
from functools import partial


DATA = os.path.join(os.path.dirname(__file__), 'data')


class HoardItem:
    """
    A random item in Whisper's Bag of Hoarding.
    """
    def __init__(self):
        self._nouns = os.path.join(DATA, 'nouns')
        self._adjectives = os.path.join(DATA, 'adjectives')
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
