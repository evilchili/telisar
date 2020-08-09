import re

from telisar.languages.base import BaseLanguage


class Orcish(BaseLanguage):

    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = ['b', 'c', 'ch', 'cht', 'd', 'f', 'h', 'k', 'm', 'n', 'p', 'r', 's', 'sh', 'sht', 't', 'x', 'z']
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
        r'b[dkprs]|' +
        r'c[hkprst]|' +
        r'd[bks]|' +
        r'f[ckrt]|' +
        r'k[rsz]|' +
        r'm[s]|' +
        r'n[stz]|' +
        r'p[st]|' +
        r'r[ktz]|' +
        r's[chkrt]|' +
        r't[chrsz]' +
        r']+\S?'
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
    syllable_template = ('C', 'V', 'c', 'c')
    first_consonants = ['b', 'c', 'd', 'k', 'p', 't', 'x', 'z']
