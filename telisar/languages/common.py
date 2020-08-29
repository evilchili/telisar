import re
import random
from telisar.languages.base import BaseLanguage, WordFactory


class Common(BaseLanguage):
    vowels = ['a', 'e', 'i', 'o', 'u']

    consonants = [
        'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't',
        'v', 'w', 'x', 'y', 'z'
    ]

    _middle_clusters = re.compile(
        r'bs|ct|ch|ck|dd|ff|gh|gs|ms|ns|ps|qu|rb|rd|rf|rk|rl|rm|rn|rp|rs|rt|ry' +
        r'|sh|sk|ss|st|sy|th|tk|ts|tt|ty|ws|yd|yk|yl|ym|yn|yp|yr|ys|yt|yz|mcd' +
        r'|[' + ''.join(vowels) + '][' + ''.join(consonants) + ']' +
        r'|[' + ''.join(consonants) + '][' + ''.join(vowels) + ']' +
        r'|[' + ''.join(vowels) + ']{1,2}'
    )

    _invalid_sequences = re.compile(
        r'[' + ''.join(vowels) + ']{3}|' +
        r'[' + ''.join(consonants) + ']{4}'
    )

    suffixes = [
        'ad', 'ed', 'id', 'od', 'ud',
        'af', 'ef', 'if', 'of', 'uf',
        'ah', 'eh', 'ih', 'oh', 'uh',
        'al', 'el', 'il', 'ol', 'ul',
        'am', 'em', 'im', 'om', 'um',
        'an', 'en', 'in', 'on', 'un',
        'ar', 'er', 'ir', 'or', 'ur',
        'as', 'es', 'is', 'os', 'us',
        'at', 'et', 'it', 'ot', 'ut',
        'ax', 'ex', 'ix', 'ox', 'ux',
        'ay', 'ey', 'iy', 'oy', 'uy',
        'az', 'ez', 'iz', 'oz', 'uz',
    ]

    prefixes = [s[::-1] for s in suffixes]

    affixes = []

    syllable_template = ('p', 'c|v', 's')

    minimum_length = 1

    def validate_sequence(self, sequence, total_syllables):
        too_short = len(''.join(sequence)) < self.minimum_length
        if too_short:
            return False

        t = ''.join(sequence)

        if self._invalid_sequences.match(t):
            self._logger.debug(f"Invalid sequence: {t}")
            return False

        for pos in range(len(t)):
            seq = t[pos:pos+2]
            if len(seq) != 2:
                return True
            if not self._middle_clusters.match(seq):
                self._logger.debug(f"Invalid sequence: {seq}")
                return False


class CommonSurname(Common):

    syllable_template = ('P|C', 'v', 'S')
    syllable_weights = [1]

    word_suffixes = [
        'berg', 'borg', 'borough', 'bury', 'berry', 'by', 'ford', 'gard', 'grave', 'grove', 'gren', 'hardt', 'hart',
        'heim', 'holm', 'land', 'leigh', 'ley', 'ly', 'lof', 'love', 'lund', 'man', 'mark', 'ness', 'olf', 'olph',
        'quist', 'rop', 'rup', 'stad', 'stead', 'stein', 'strom', 'thal', 'thorpe', 'ton', 'vall', 'wich', 'win',
        'some', 'smith', 'bridge', 'cope', 'town', 'er', 'don', 'den', 'dell', 'son',
    ]

    def word(self):
        return str(WordFactory(self)) + random.choice(self.word_suffixes)


class CommonPerson(Common):

    syllable_template = ('p', 'C', 'V', 's')
    syllable_weights = [3, 1]

    minimum_length = 2

    def person(self):
        return (WordFactory(language=self), CommonSurname().word())
