import re
import random
from collections import namedtuple

# represent langauge data
phoneme = namedtuple('Phoneme', ['graphemes', 'weights', 'pattern'])

class Name:
    """
    A single randomly-generated name.

    Example Usage:

        > name = Name(('c', 'V'), [1, 1], vowels, consonants, affixes)
        > name.as_string
        Some Name

    Names are created by combining syllables selected from random phonemes according to templates, each containing one
    or more of the following:

        c - an optional consonant
        C - a required consonant
        v - an optional vowel
        V - a required consonant

    The simplest possible syllable therefore consists of a single grapheme.

    Names can also be generated from affixes; these are specified by the special template specifiers 'a'/'A'.

    Examples:

        ('c', 'V')           - a syllable consisting of exactly one vowel, possibly preceeded by a single consonant
        ('C', 'c', 'V', 'v') - a syllable consisting of one or two consonants followed by one or two vowels
        ('a', 'C', 'V')      - a syllable consisting of an optional affix, a consonant and a vowel.

    Name length is determined by the number of syllables, which is chosen at random using relative weights:

        [2, 2, 1] - Names may contain one, two or three syllables, but are half as likely to contain three.
        [0, 1]    - Names must have exactly two syllables

    Instance Properties:

        as_string (str): The name as a string
        syllables (int): The number of syllables randomly selected for this name

    """
    def __init__(self, template, weights, vowels, consonants, affixes):
        """
        Construtor.

        Args:
            template (iter): the syllable template to use
            weights (iter): syllable weights
            vowels (phoneme): valid vowels
            consonants (phoneme): valid consonants
            affixes (phoneme): valid affixes
        """
        self._weights = weights
        self._templates = template
        self._vowels = vowels
        self._consonants = consonants
        self._affixes = affixes

        self._syllables = 0
        self._as_string = ''

    @property
    def syllables(self):
        """
        Return a random number of syllables for a single name using the specified weights.
        """
        if not self._syllables:
            self._syllables = 1 + random.choices(range(len(self._weights)), self._weights)[0]
        return self._syllables

    @property
    def as_string(self):
        """
        Return a randomly-generated name.
        """
        if not self._as_string:
            name = ''
            while not name:
                for _ in range(self.syllables):
                    name = name + self._make_syllable()
                if name:
                    self._as_string = name
                    break
                else:
                    name = ''
        return self._as_string

    def _make_syllable(self):
        """
        Generate a single syllable of a name, using syllable templates
        """
        syllable = ''
        for part in self._templates:
            syllable = syllable + self._random_grapheme(part)
        return syllable

    def _random_grapheme(self, phoneme_type):
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
            return random.choices(self._consonants.graphemes, self._consonants.weights)[0]
        elif pt == 'v':
            return random.choices(self._vowels.graphemes, self._vowels.weights)[0]
        elif pt == 'a':
            return random.choices(self._affixes.graphemes, self._affixes.weights)[0]
        raise Exception(f"Invalid phoneme type: {phoneme_type}")

    def __str__(self):
        return self.as_string


class Generator:
    """
    Random name generator. This class loads language data from text files and generates Name instances.

    Instance Attributes:

        validator (callable): A method used to validate a generated name
        people (str): The people whose language should be used (e.g., 'elf')
        data_path (str): the path to the language data files for the people
    """

    def __init__(self, people='', validator=None, data_path='data'):
        """
        Constructor.

        people (str): The people whose language should be used (e.g., 'elf')
        validator (callable): A method used to validate a generated name
        data_path (str): the path to the language data files for the people
        """
        self.validator = validator
        self.people = people
        self.data_path = data_path

        self._cache = {}
        self._load_graphemes()

    def generate(self, template, weights):
        """
        Generate a single name using the specified syllable template and weights.

        Args:
            template (iter): An iterable of syllable templates.
            weights (iter): An iterable of syllable weights as integers.

        Refer to the Name class's docs for a description of possible templates and weights.

        Returns:
            string: A randomly-generated name that has passed validation.
        """
        name = None
        while not name:
            name = Name(template, weights, **self._cache)
            if callable(self.validator) and not self.validator(name):
                name = ''
                continue
            return name.as_string

    def _get_path(self, phoneme):
        return f"{self.data_path}/{self.people}_{phoneme}"

    def _load_graphemes(self):
        """
        Load data files and cache the language components as phoneme instances.
        """
        with open(self._get_path('vowels')) as f:
            vowels = [l.strip() for l in f.readlines()]
            self._cache['vowels'] = phoneme(
                graphemes=vowels,
                weights=[1 * len(v) for v in vowels],
                pattern=re.compile(r'[' + r'|'.join(vowels) + r']')
            )
        with open(self._get_path('consonants')) as f:
            consonants = [l.strip() for l in f.readlines()]
            self._cache['consonants'] = phoneme(
                graphemes=consonants,
                weights=[1 * len(c) for c in consonants],
                pattern=re.compile(r'[' + r'|'.join(consonants) + r']')
            )
        self._load_affixes()

    def _load_affixes(self):
        """
        Load affixes, if they exist and cache them as a phoneme instance.
        """
        try:
            with open(self._get_path('affixes')) as f:
                affixes = [l.strip() for l in f.readlines()]
                self._cache['affixes'] = phoneme(
                    graphemes=affixes,
                    weights=[1 for _ in affixes],
                    pattern=re.compile(r'[' + r'|'.join(affixes) + r']')
                )
        except OSError:
            return
