import re

from telisar.languages.base import BaseLanguage


class Elven(BaseLanguage):

    _vowels = ['a', 'e', 'i', 'o', 'u', 'á', 'é', 'i', 'o', 'u']
    _consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'l', 'k', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'y']
    _affixes = ['am', 'an', 'al']

    _valid_middle_clusters = re.compile(
        r'^\S?[cc|ht|hty|kd|kl|km|kp|kt|kv|kw|ky|lc|ld|lf|ll|lm|lp|lt|lv|lw|ly|mb|mm|mp|my|' +
        r'nc|nd|ng|ngw|nn|nt|nty|nw|ny|ps|pt|rc|rd|rm|rn|rp|rqu|rr|rs|rt|rty|rw|ry|sc|squ|ss|ts|tt|tw|ty]+\S?$'
    )

    def is_valid_word(self, word):

        # elven affixes are words
        if self.is_valid_affix(word):
            return True

        return (
            self._validate_first_syllable(word) and
            self._validate_middle_clusters(word) and
            self._validate_last_syllable(word)
        )

    def person_name(self):
        templates = [
            (('c', 'V', 'c'), [0, 1, 2]),
            ('A', [1])
        ]
        names = []
        for (template, weights) in templates:
            names.append(self.word(template, weights))
        names.append(self.place_name())
        return names

    def place_name(self):
        return self.word(('c', 'V', 'c'), [0, 2, 2])

    def _validate_first_syllable(self, word):

        # anything starting with a vowel is fine
        if self.is_valid_vowel(word[0]):
            return True

        # anything starting with these sequences is fine
        valid = re.compile(r'[ky|ty|ly|ny|nw]')
        if valid.match(word[:2]):
            return True

        # anything starting with one of these consonants followed by a vowel is fine
        if word[0] in 'cfhlmnpqrstvwy':
            if self.is_valid_vowel(word[1]):
                return True

        return False

    def _validate_last_syllable(self, word):
        if word[-1] not in ['t', 's', 'n', 'l', 'r']:
            if not self.is_valid_vowel(word[-1]):
                return False
        return True

    def _validate_middle_clusters(self, word):
        last_consonant = ''
        for char in word:
            if char in [v.char for v in self.vowels]:
                last_consonant = ''
                continue
            if last_consonant:
                if not self._valid_middle_clusters.match(last_consonant + char):
                    return False
            last_consonant = char
        return True
