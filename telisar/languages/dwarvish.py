import random

from telisar.languages.base import BaseLanguage


class Dwarvish(BaseLanguage):

    consonants = [
        'b', 'p', 'ph', 'd', 't', 'th', 'j', 'c', 'ch', 'g', 'k', 'kh', 'v', 'f', 'z', 's', 'zh', 'sh', 'hy', 'h', 'r',
        'l', 'y', 'w', 'm', 'n'
    ]

    vowels = [
        'a', 'e', 'i', 'o', 'u', 'î', 'ê', 'â', 'û', 'ô'
    ]

    affixes = []

    first_consonants = consonants
    first_vowels = vowels
    first_affixes = affixes

    last_vowels = vowels
    last_consonants = consonants
    last_affixes = affixes

    syllable_template = ('C', 'V', 'c')
    syllable_weights = [4, 1]

    name_suffixes = ['son', 'sson', 'zhon', 'dottir', 'dothir', 'dottyr']

    def person(self):
        words = super().person()
        suffix = random.choice(Dwarvish.name_suffixes)
        return (str(words[0]), f"{words[1]}{suffix}")

    def is_valid(self, text):
        for suffix in self.name_suffixes:
            if text.endswith(suffix):
                text = text[0:len(suffix)]
                break
        return super().is_valid(text)
