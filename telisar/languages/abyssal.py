from telisar.languages.base import BaseLanguage
import re


class Abyssal(BaseLanguage):

    vowels = ['a', 'e', 'i', 'o', 'u', 'î', 'ê', 'â', 'û', 'ô', 'ä', 'ö', 'ü', 'äu', 'ȧ', 'ė', 'ị', 'ȯ', 'u̇']

    consonants = ['c', 'g', 'j', 'k', 'p', 'ss', 't']

    syllable_template = ('V', 'v', 'c', 'v')

    _invalid_sequences = re.compile(
        r'[' + ''.join(vowels) + ']{5}|' +
        r'[' + ''.join(consonants) + ']{3}'
    )

    syllable_weights = [3, 2]

    minimum_length = 2

    def validate_sequence(self, sequence, total_syllables):
        too_short = len(''.join(sequence)) < self.minimum_length
        if too_short:
            return False

        t = ''.join(sequence)

        if self._invalid_sequences.match(t):
            self._logger.debug(f"Invalid sequence: {t}")
            return False
        return True
