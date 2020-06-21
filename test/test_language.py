import pytest
import itertools

from telisar.languages.base import BaseLanguage


@pytest.fixture
def test_lang():
    class _(BaseLanguage):
        vowels = 'ae'
        consonants = 'bcd'
        affixes = 'o'

        first_vowels = vowels
        first_consonants = consonants
        first_affixes = affixes

        last_vowels = vowels
        last_consonants = consonants
        last_affixes = affixes

        syllable_template = ('C', 'V')
        syllable_weights = [1, 1]

        minimum_length = 2
    return _


def possible_syllables(klass):
    return [x[0]+x[1] for x in itertools.product(klass.consonants, klass.vowels)]


def possible_words(klass):
    syllables = possible_syllables(klass)
    return (
        [''.join(x) for x in itertools.combinations(syllables, 1)] +
        [''.join(x) for x in itertools.product(syllables, syllables)]
    )


def test_BaseLanguage_is_valid(test_lang):
    lang = test_lang()
    for word in possible_words(test_lang):
        assert lang.is_valid(word)
        assert lang.is_valid(f"x{word}") is False
        assert lang.is_valid(f"{word}x") is False
