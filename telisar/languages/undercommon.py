import random
import re

from telisar.languages.base import BaseLanguage, WordFactory


class Undercommon(BaseLanguage):
    vowels = ['a', 'e', 'i', 'o', 'u', 'a', 'e', 'i', 'o', 'u', 'ä', 'ö', 'ü', 'äu']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'y', 'z']
    affixes = []

    first_vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    first_consonants = ['c', 'g', 'l', 'm', 'n', 'r', 's', 't', 'v', 'z']
    first_affixes = []

    last_vowels = ['a', 'i', 'e']
    last_consonants = ['t', 's', 'm', 'n', 'l', 'r', 'd', 'a', 'th']
    last_affixes = []

    syllable_template = ('c', 'v', 'c', 'V', 'C', 'v')
    minimum_length = 4

    _valid_consonant_sequences = [
        'cc', 'ht', 'kd', 'kl', 'km', 'kp', 'kt', 'kv', 'kw', 'ky', 'lc', 'ld',
        'lf', 'll', 'lm', 'lp', 'lt', 'lv', 'lw', 'ly', 'mb', 'mm', 'mp', 'my',
        'nc', 'nd', 'ng', 'nn', 'nt', 'nw', 'ny', 'ps', 'pt', 'rc', 'rd', 'rm',
        'rn', 'rp', 'rr', 'rs', 'rt', 'rw', 'ry', 'sc', 'ss', 'ts', 'tt', 'th',
        'tw', 'ty'
    ]

    _invalid_sequences = re.compile(
        r'[' + ''.join(vowels) + ']{3}|' +
        r'[' + ''.join(consonants) + ']{4}'
    )

    def validate_sequence(self, sequence, *args, **kwargs):
        """
        Ensure the specified sequence of syllables results in valid letter combinations.
        """
        too_short = len(''.join(sequence)) < self.minimum_length
        if too_short:
            return False

        # the whole string must be checked against the invalid sequences pattern
        chars = ''.join(sequence)
        if self._invalid_sequences.match(chars):
            self._logger.debug(f"Invalid sequence: {chars}")
            return False

        # Now step through the sequence, two letters at a time, and verify that
        # all pairs of consonants are valid.
        for offset in range(0, len(chars), 2):
            seq = chars[offset:2]
            if not seq:
                break
            if seq[0] in self.consonants and seq[1] in self.consonants:
                if seq not in self._valid_consonant_sequences:
                    self._logger.debug(f"Invalid sequence: {seq}")
                    return False

        return True


class DrowPlaceName(Undercommon):
    syllable_template = ('v', 'C', 'v')
    syllable_weights = [2, 1]
    first_consonants = Undercommon.first_consonants + ['q']

    minimum_length = 2

    affixes = ['el']

    def word(self):
        prefix = str(WordFactory(self))
        suffix = []
        while not self.validate_sequence(suffix):
            suffix = [
                random.choice(self.last_vowels),
                random.choice(self.last_consonants + ['ss']),
            ]
        return prefix + ''.join(suffix)

    def full_name(self):
        return 'el '.join(self.names)


class DrowSurname(Undercommon):
    syllable_template = ('v', 'C', 'v')
    syllable_weights = [1, 2, 2]
    minimum_length = 2

    def word(self):
        prefix = str(WordFactory(self))
        suffix = ''
        while not self.validate_sequence(suffix):
            suffix = ''.join([
                random.choice(self.last_vowels),
                random.choice(self.last_consonants + ['ss']),
                random.choice([
                    'ie',
                    'ia',
                    'io',
                ]),
                random.choice(['th', 's', 'r', 'n'])
            ])
        return prefix + suffix


class DrowPerson(Undercommon):
    syllable_template = ('c', 'V', 'C', 'v')
    syllable_weights = [1, 2]

    def place(self):
        return DrowPlaceName().word()

    def word(self):
        return (
            super().word(),
            DrowSurname().word(),
        )

    person = word
