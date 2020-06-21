import random
import re

from telisar.languages.base import BaseLanguage


class Elven(BaseLanguage):
    """
    Phonetics for the Elven language in Telisar. Loosely based on Tolkein's Quenya language, but with character tweaks
    and naming conventions following Twirrim's conventions in-game.
    """

    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y', 'z']
    affixes = []

    first_vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    first_consonants = ['c', 'g', 'l', 'm', 'n', 'r', 's', 't', 'v', 'z']
    first_affixes = []

    last_vowels = ['a', 'i', 'e']
    last_consonants = ['t', 's', 'm', 'n', 'l', 'r', 'd', 'a', 'th']
    last_affixes = []

    _middle_clusters = re.compile(
        r'\S?[cc|ht|hty|kd|kl|km|kp|kt|kv|kw|ky|lc|ld|lf|ll|lm|lp|lt|lv|lw|ly|mb|mm|mp|my|' +
        r'nc|nd|ng|ngw|nn|nt|nty|nw|ny|ps|pt|rc|rd|rm|rn|rp|rqu|rr|rs|rt|rty|rw|ry|sc|squ|ss|ts|tt|th|tw|ty]+\S?'
    )

    def validate_sequence(self, sequence, total_syllables):
        too_short = len(''.join(sequence)) < self.minimum_length
        if too_short:
            return False
        seq = ''.join(sequence[-2:])
        if not self._middle_clusters.match(seq):
            self._logger.debug(f"Invalid sequence: {sequence[-2:]}")
            return False
        return True


class ElvenPlaceName(Elven):
    syllable_template = ('c', 'V', 'v', 'c')
    syllable_weights = [1, 2]

    def full_name(self):
        return 'el '.join(self.names)


class ElvenPerson(Elven):

    syllable_template = ('c', 'V', 'C', 'v')
    syllable_weights = [0, 2, 2]

    last_affixes = ['am', 'an', 'al', 'um']

    def word(self):
        return (
            super().word(),
            random.choice(self.last_affixes),
            ElvenPlaceName().word()
        )
