import pytest
import itertools

from telisar.languages.base import BaseLanguage


@pytest.fixture
def test_lang():
    class _(BaseLanguage):
        _vowels = 'ae'
        _consonants = 'bcd'
        _affixes = 'o'

        syllable_template = ('C', 'V')
        syllable_weights = [1, 1]

    return _


def possible_syllables(klass):
    return [x[0]+x[1] for x in itertools.product(klass._consonants, klass._vowels)]


def possible_words(klass):
    syllables = possible_syllables(klass)
    return (
        [''.join(x) for x in itertools.combinations(syllables, 1)] +
        [''.join(x) for x in itertools.product(syllables, syllables)]
    )


def test_BaseLanguage_init(test_lang):
    lang = test_lang()
    assert lang.vowels
    assert lang.consonants
    assert lang.affixes

    assert lang.is_valid_vowel('a')
    assert lang.is_valid_vowel('e')
    assert lang.is_valid_consonant('b')
    assert lang.is_valid_consonant('c')
    assert lang.is_valid_consonant('d')
    assert lang.is_valid_affix('o')

    assert lang.is_valid_grapheme('x') is False


def test_word_with_defaults(test_lang):
    lang = test_lang()
    possible = possible_words(test_lang)
    for _ in range(100):
        assert lang.word() in possible
