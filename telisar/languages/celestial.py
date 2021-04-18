from telisar.languages.base import BaseLanguage
import re


class Celestial(BaseLanguage):

    vowels = ['a', 'e', 'i', 'o', 'u', 'î', 'ê', 'â', 'û', 'ô', 'ä', 'ö', 'ü', 'äu', 'ȧ', 'ė', 'ị', 'ȯ', 'u̇']

    consonants = ['b', 'sc', 'f', 'h', 'l', 'm', 'n', 'r', 's', 'v']

    syllable_template = ('V', 'v', 'c', 'c', 'v', 'v')

    _invalid_sequences = re.compile(
        r'[' + ''.join(vowels) + ']{5}|' +
        r'[' + ''.join(consonants) + ']{3}'
    )

    syllable_weights = [3, 2]

    minimum_length = 5

    def validate_sequence(self, sequence, total_syllables):
        too_short = len(''.join(sequence)) < self.minimum_length
        if too_short:
            return False

        t = ''.join(sequence)

        if self._invalid_sequences.match(t):
            self._logger.debug(f"Invalid sequence: {t}")
            return False
        return True
