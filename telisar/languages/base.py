import random
import logging
from collections import namedtuple

grapheme = namedtuple('Grapheme', ['char', 'weight'])


class LanguageException(Exception):
    """
    Thrown when language validators fail.
    """


class SyllableFactory:

    def __init__(self, template, weights, vowels, consonants, affixes):
        self.template = template
        self.weights = weights
        self.grapheme = {
            'chars': {
                'c': [x.char for x in consonants],
                'v': [x.char for x in vowels],
                'a': [x.char for x in affixes]
            },
            'weights': {
                'c': [x.weight for x in consonants],
                'v': [x.weight for x in vowels],
                'a': [x.weight for x in affixes]
            }
        }

    def graphemes(self):
        for chars in [v for v in self.grapheme['chars'].values()]:
            for char in chars:
                yield char

    def is_valid(self, chars):
        return (
            chars in self.grapheme['chars']['c'] or
            chars in self.grapheme['chars']['v'] or
            chars in self.grapheme['chars']['a']
        )

    def get(self):
        """
        Generate a single syllable
        """
        syllable = ''
        for t in self.template:
            if t.islower() and random.random() < 0.5:
                continue
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
            seq = [self.language.first_syllable.get()]
            while len(seq) < total_syllables - 2:
                seq.append(self.language.syllable.get())
            if len(seq) < total_syllables:
                seq.append(self.language.last_syllable.get())
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

    vowels = []
    consonants = []
    affixes = []

    first_vowels = vowels
    first_consonants = consonants
    first_affixes = affixes

    last_vowels = vowels
    last_consonants = consonants
    last_affixes = affixes

    syllable_template = ('C', 'V')
    syllable_weights = [1, 1]

    minimum_length = 3

    def __init__(self):
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)

        self.syllable = SyllableFactory(
            template=self.syllable_template,
            weights=self.syllable_weights,
            vowels=[grapheme(char=c, weight=1) for c in self.__class__.vowels],
            consonants=[grapheme(char=c, weight=1) for c in self.__class__.consonants],
            affixes=[grapheme(char=c, weight=1) for c in self.__class__.affixes]
        )

        self.first_syllable = SyllableFactory(
            template=self.syllable_template,
            weights=self.syllable_weights,
            vowels=[grapheme(char=c, weight=1) for c in self.__class__.first_vowels],
            consonants=[grapheme(char=c, weight=1) for c in self.__class__.first_consonants],
            affixes=[grapheme(char=c, weight=1) for c in self.__class__.first_affixes]
        )

        self.last_syllable = SyllableFactory(
            template=self.syllable_template,
            weights=self.syllable_weights,
            vowels=[grapheme(char=c, weight=1) for c in self.__class__.last_vowels],
            consonants=[grapheme(char=c, weight=1) for c in self.__class__.last_consonants],
            affixes=[grapheme(char=c, weight=1) for c in self.__class__.last_affixes]
        )


    def _valid_syllable(self, syllable, text, reverse=False):
        length = 0
        for seq in syllable.graphemes():
            length = len(seq)
            substr = text[-1 * length:] if reverse else text[0:length]
            if substr == seq:
                return length
        return False

    def is_valid(self, text):

        affixes = set(self.affixes + self.first_affixes + self.last_affixes)
        for part in text.lower().split(' '):

            if part in affixes:
                continue

            if len(part) < self.minimum_length:
                self._logger.debug(f"'{part}' too short; must be {self.minimum_length} characters.")
                return False

            first_offset = self._valid_syllable(self.first_syllable, part)
            if first_offset is False:
                self._logger.debug(f"'{part}' is not a valid syllable.")
                return False

            last_offset = self._valid_syllable(self.last_syllable, part, reverse=True)
            if last_offset is False:
                self._logger.debug(f"'{part}' is not a valid syllable.")
                return False
            last_offset = len(part) - last_offset

            while first_offset < last_offset:
                middle = part[first_offset:last_offset]
                new_offset = self._valid_syllable(self.syllable, middle)
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
