import random
import logging
from collections import namedtuple

grapheme = namedtuple('Grapheme', ['char', 'weight'])


class LanguageException(Exception):
    """
    Thrown when language validators fail.
    """


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

    _vowels = []
    _consonants = []
    _affixes = []

    syllable_template = ('C', 'V')
    syllable_weights = [1, 1]

    def __init__(self, vowels=None, consonants=None, affixes=None):
        self._logger = logging.getLogger('language')
        self._logger.setLevel(logging.ERROR)
        self._load_graphemes(vowels, consonants, affixes)

    @property
    def vowels(self):
        return self._vowels

    @property
    def consonants(self):
        return self._consonants

    @property
    def affixes(self):
        return self._affixes

    def is_valid_affix(self, sequence):
        if sequence.lower() not in [g.char for g in self.affixes]:
            raise LanguageException(f"Invalid affix: {sequence.lower()}")
        return True

    def is_valid_vowel(self, sequence):
        if sequence.lower() not in [g.char for g in self.vowels]:
            raise LanguageException(f"Invalid vowel: {sequence.lower()}")
        return True

    def is_valid_consonant(self, sequence):
        if sequence.lower() not in [g.char for g in self.consonants]:
            raise LanguageException(f"Invalid consonant: {sequence.lower()}")
        return True

    def is_valid_grapheme(self, sequence):
        return (
            self.is_valid_affix(sequence) or
            self.is_valid_vowel(sequence) or
            self.is_valid_consonant(sequence)
        )

    def is_valid_word(self, word):
        raise NotImplementedError("You must define is_valid_word() on your subclass.")

    def person_name(self):
        return self.word()

    def place_name(self):
        return self.word()

    def word(self, syllable_template=None, syllable_weights=None, vowels=None, consonants=None, affixes=None):

        # handle overrides
        if not syllable_template:
            syllable_template = self.syllable_template
        if not syllable_weights:
            syllable_weights = self.syllable_weights
        if not vowels:
            vowels = self.vowels
        if not consonants:
            consonants = self.consonants
        if not affixes:
            affixes = self.affixes

        # select a random number of syllables for this word
        syllable_count = 1 + random.choices(range(len(syllable_weights)), syllable_weights)[0]

        # generate a valid word by combining syllables
        word = ''
        while not (word and self.is_valid_word(word)):
            word = ''.join([
                self._syllable(syllable_template, syllable_weights, vowels, consonants, affixes)
                for _ in range(syllable_count)
            ])
        return word

    def _syllable(self, template, weights, vowels, consonants, affixes):
        """
        Generate a single syllable
        """
        syllable = ''
        for part in template:
            syllable = syllable + self._random_grapheme(part, vowels, consonants, affixes)
        return syllable

    def _load_graphemes(self, vowels, consonants, affixes):
        if vowels:
            self._vowels = vowels
        else:
            self._vowels = [grapheme(char=c, weight=1) for c in self.__class__._vowels]

        if consonants:
            self._consonants = consonants
        else:
            self._consonants = [grapheme(char=c, weight=1) for c in self.__class__._consonants]

        if affixes:
            self._affixes = affixes
        else:
            self._affixes = [grapheme(char=c, weight=1) for c in self.__class__._affixes]

    def _random_grapheme(self, phoneme_type, vowels, consonants, affixes):
        """
        Randomly choose a grapheme of the given type, weighted by length; graphemes of 2 characters are half as likely
        to be selected as graphemes of 1 character, and so on.

        Args:
            phoneme_type (str): The type of grapheme to select; 'c' or 'C' for a consonant, 'v' or 'V' for a vowel. The
                special values 'a' and 'A' can be used to select an affix, if available. If the phoneme_type is in
                lower-case, there is a 50% chance an empty string will ber returned instead of a grapheme.

        Returns:
            string: a grapheme of the specified type.
        """
        if phoneme_type.islower() and random.random() < 0.5:
            return ''
        pt = phoneme_type.lower()
        if pt == 'c':
            return self._pick_one_grapheme(consonants)
        elif pt == 'v':
            return self._pick_one_grapheme(vowels)
        elif pt == 'a':
            return self._pick_one_grapheme(affixes)
        raise Exception(f"Invalid phoneme type: {phoneme_type}")

    def _pick_one_grapheme(self, graphemes):
        # this is brute force and stupid -- by default all graphemes are weighted equally,
        # which is totally not how actual languages work. But I'm invoking Rule 0 because Rule 0.
        return random.choices([g.char for g in graphemes], [g.weight for g in graphemes])[0]
