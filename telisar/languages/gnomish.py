from telisar.languages.base import BaseLanguage


class Gnomish(BaseLanguage):

    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    consonants = ['b', 'd', 'f', 'g', 'h', 'j', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'z']
    affixes = []

    first_vowels = vowels
    first_consonants = consonants
    first_affixes = affixes

    last_vowels = ['a', 'e', 'i', 'o', 'y']
    last_consonants = consonants
    last_affixes = affixes

    syllable_template = ('C', 'V', 'v')
    syllable_weights = [3, 1]

    minimum_length = 1

    def person(self):
        return (self.word(), self.word())
