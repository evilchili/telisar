import random
import logging
from collections import namedtuple

grapheme = namedtuple('Grapheme', ['char', 'weight'])


class LanguageException(Exception):
    """
    Thrown when language validators fail.
    """


class SyllableFactory:

    def __init__(self, template, weights, prefixes, vowels, consonants, suffixes, affixes):
        self.template = template
        self.weights = weights
        self.grapheme = {
            'chars': {
                'p': [x.char for x in prefixes],
                'c': [x.char for x in consonants],
                'v': [x.char for x in vowels],
                's': [x.char for x in suffixes],
                'a': [x.char for x in affixes]
            },
            'weights': {
                'p': [x.weight for x in prefixes],
                'c': [x.weight for x in consonants],
                'v': [x.weight for x in vowels],
                's': [x.weight for x in suffixes],
                'a': [x.weight for x in affixes]
            }
        }

    def _filtered_graphemes(self, key):
        return [(k, v) for (k, v) in self.grapheme['chars'].items() if k in key]

    def graphemes(self, key='apcvs'):
        for _, chars in self._filtered_graphemes(key):
            for char in chars:
                yield char

    def is_valid(self, chars, key='apcvs'):
        for grapheme_type, _ in self._filtered_graphemes(key):
            if chars in self.grapheme['chars'][grapheme_type]:
                return True
        return False

    def get(self):
        """
        Generate a single syllable
        """
        syllable = ''
        for t in self.template:
            if t.islower() and random.random() < 0.5:
                continue
            if '|' in t:
                t = random.choice(t.split('|'))
            t = t.lower()
            syllable = syllable + random.choices(self.grapheme['chars'][t], self.grapheme['weights'][t])[0]
        return syllable

    def __str__(self):
        return self.get()


class WordFactory:

    def __init__(self, language):
        self.language = language

    def random_syllable_count(self):
        return 1 + random.choices(range(len(self.language.syllable.weights)), self.language.syllable.weights)[0]

    def get(self):

        total_syllables = self.random_syllable_count()
        seq = []
        while not self.language.validate_sequence(seq, total_syllables):
            seq = [self.language.syllable.get()]
            while len(seq) < total_syllables - 2:
                seq.append(self.language.syllable.get())
            if len(seq) < total_syllables:
                seq.append(self.language.syllable.get())
        return ''.join(seq)

    def __str__(self):
        return self.get()


class BaseLanguage:
    """
    Words are created by combining syllables selected from random phonemes according to templates, each containing one
    or more of the following grapheme indicators:

        c - an optional consonant
        C - a required consonant
        v - an optional vowel
        V - a required consonant

    The simplest possible syllable consists of a single grapheme, and the simplest possible word a single syllable.

    Words can also be generated from affixes; these are specified by the special template specifiers 'a'/'A'.

    Examples:

        ('c', 'V')           - a syllable consisting of exactly one vowel, possibly preceeded by a single consonant
        ('C', 'c', 'V', 'v') - a syllable consisting of one or two consonants followed by one or two vowels
        ('a', 'C', 'V')      - a syllable consisting of an optional affix, a consonant and a vowel.

    Word length is determined by the number of syllables, which is chosen at random using relative weights:

        [2, 2, 1] - Names may contain one, two or three syllables, but are half as likely to contain three.
        [0, 1]    - Names must have exactly two syllables
    """

    affixes = []
    vowels = []
    consonants = []

    prefixes = vowels + consonants
    suffixes = vowels + consonants

    syllable_template = ('C', 'V')
    syllable_weights = [1, 1]

    minimum_length = 3

    def __init__(self):
        self._logger = logging.getLogger()

        self.syllable = SyllableFactory(
            template=self.syllable_template,
            weights=self.syllable_weights,
            prefixes=[grapheme(char=c, weight=1) for c in self.__class__.prefixes],
            suffixes=[grapheme(char=c, weight=1) for c in self.__class__.suffixes],
            vowels=[grapheme(char=c, weight=1) for c in self.__class__.vowels],
            consonants=[grapheme(char=c, weight=1) for c in self.__class__.consonants],
            affixes=[grapheme(char=c, weight=1) for c in self.__class__.affixes]
        )


    def _valid_syllable(self, syllable, text, key='apcvs', reverse=False):
        length = 0
        for seq in reverse(sorted(syllable.graphemes(key=key), key=len)):
            length = len(seq)
            substr = text[-1 * length:] if reverse else text[0:length]
            if substr == seq:
                return length
        return False

    def is_valid(self, text):

        for part in text.lower().split(' '):

            if part in self.affixes:
                continue

            if len(part) < self.minimum_length:
                self._logger.debug(f"'{part}' too short; must be {self.minimum_length} characters.")
                return False

            first_offset = self._valid_syllable(self.syllable, text=part, key='p')
            if first_offset is False:
                self._logger.debug(f"'{part}' is not a valid syllable.")
                return False

            last_offset = self._valid_syllable(self.last_syllable, text=part, key='s', reverse=True)
            if last_offset is False:
                self._logger.debug(f"'{part}' is not a valid syllable.")
                return False
            last_offset = len(part) - last_offset

            while first_offset < last_offset:
                middle = part[first_offset:last_offset]
                new_offset = self._valid_syllable(self.syllable, text=middle, key='cv')
                if new_offset is False:
                    self._logger.debug(f"'{middle}' is not a valid middle sequence.")
                    return False
                first_offset = first_offset + new_offset
        return True

    def validate_sequence(self, sequence, total_syllables):
        return len(''.join(sequence)) > self.minimum_length

    def word(self):
        return WordFactory(language=self)

    def place(self):
        return self.word()

    def person(self):
        return (self.word(), self.word())
