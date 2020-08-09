import re

from telisar.languages.base import BaseLanguage


class Orcish(BaseLanguage):

    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = ['b', 'c', 'ch', 'd', 'f', 'h', 'k', 'm', 'n', 'p', 'r', 's', 'sh', 't', 'z']
    affixes = []

    first_vowels = vowels
    first_consonants = consonants
    first_affixes = affixes

    last_vowels = vowels
    last_consonants = consonants
    last_affixes = affixes

    syllable_template = ('C', 'c', 'V')
    syllable_weights = [2, 4, 0.5]

    _middle_clusters = re.compile(
        r'\S?[' +
        r'bd|bk|br|bs|' +
        r'ch|ck|cp|cr|cs|ct|' +
        r'db|dk|ds|' +
        r'fr|ft|' +
        r'kr|ks|kz|' +
        r'ms|' +
        r'ns|nt|nz|' +
        r'ps|pt|' +
        r'rk|rt|rz|' +
        r'sc|sh|sk|sr|st|' +
        r'tc|th|tr|ts|tz' +
        r']\S?'
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


class OrcishPerson(Orcish):
    pass


class HalfOrcPerson(Orcish):
    syllable_template = ('C', 'V', 'c')
    first_consonants = ['b', 'c', 'd', 'k', 'p', 't', 'z']
    last_consonants = Orcish.consonants + ['sht', 'cht', 'zt', 'zch']
