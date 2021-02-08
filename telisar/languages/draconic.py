from telisar.languages.base import BaseLanguage, WordFactory
import random
import re


class Draconic(BaseLanguage):

    vowels = ["a'", "aa", "ah", "e'", "ee", "ei", "ey", "i'", "ii", "ir", "o'", "u'", "uu"]

    consonants = [
        'd', 'f', 'g', 'h', 'j', 'k', 'l',
        'n', 'r', 's', 't', 'v', 'x', 'y', 'z',
    ]

    syllable_template = ('C', 'V')

    _invalid_sequences = re.compile(
        r'[' + ''.join(vowels) + ']{3}|' +
        r'[' + ''.join(consonants) + ']{4}'
    )

    syllable_weights = [0, 0, 1, 2, 2, 1]

    minimum_length = 3

    def validate_sequence(self, sequence, total_syllables):
        too_short = len(''.join(sequence)) < self.minimum_length
        if too_short:
            return False

        t = ''.join(sequence)

        if self._invalid_sequences.match(t):
            self._logger.debug(f"Invalid sequence: {t}")
            return False
        return True


class Dragon(Draconic):

    syllable_template = ('v', 'C', 'V')
    syllable_weights = [0, 1, 2]

    vowels = ['a', 'e', 'i', 'o', 'u']
    last_vowels = vowels
    last_consonants = ['th', 'x', 'ss', 'z']

    minimum_length = 2

    _invalid_sequences = re.compile(
        r'[' + ''.join(last_vowels) + ']{2}|' +
        r'[' + ''.join(Draconic.consonants) + ']{2}'
    )

    def names(self):
        prefix = str(WordFactory(self))
        suffix = ''
        while not self.validate_sequence(suffix, 1):
            suffix = ''.join([
                random.choice(self.last_vowels),
                random.choice(self.last_consonants),
                random.choice(['us', 'ux', 'as', 'ax', 'is', 'ix', 'es', 'ex'])

            ])
        return [prefix + suffix]

    person = names
