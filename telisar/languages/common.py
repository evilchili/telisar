import random

from telisar.languages.base import BaseLanguage, WordFactory


class Common(BaseLanguage):
    vowels = ['a', 'e', 'i', 'o', 'u']

    first_consonants = vowels + [
        'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'y', 'z'
    ]

    consonants = [
        'b', 'bs', 'ct', 'ch', 'ck', 'ct', 'd', 'dd', 'f', 'ff', 'g', 'gh', 'gs', 'h', 'k', 'l', 'm', 'ms', 'n', 'ns',
        'p', 'ps', 'r',  'rb', 'rd', 'rf', 'rk', 'rl', 'rm', 'rn', 'rp', 'rs', 'rt', 'ry', 's', 'sh', 'sk', 'ss', 'st',
        'sy', 't', 'th', 'tk', 'ts', 'tt', 'ty', 'v', 'w', 'ws', 'x', 'y', 'yd', 'yk', 'yl', 'ym', 'yn', 'yp', 'yr',
        'ys', 'yt', 'yz', 'z', 'cd',
    ]

    last_vowels = vowels + [
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

    affixes = []

    first_vowels = vowels
    first_affixes = affixes

    last_consonants = consonants
    last_affixes = affixes

    syllable_template = ('C', 'V')
    syllable_weights = [1, 6, 4]

    minimum_length = 2


    def validate_sequence(self, sequence, total_syllables):
        return len(''.join(sequence)) >= self.minimum_length


class CommonPerson(Common):

    syllable_template = ('C', 'V')
    syllable_weights = [0, 5, 1]

    last_vowels = [
        'berg', 'borg', 'borough', 'bury', 'berry', 'by', 'ford', 'gard', 'grave', 'grove', 'gren', 'hardt', 'hart',
        'heim', 'holm', 'land', 'leigh', 'ley', 'ly', 'lof', 'love', 'lund', 'man', 'mark', 'ness', 'olf', 'olph',
        'quist', 'rop', 'rup', 'stad', 'stead', 'stein', 'strom', 'thal', 'thorpe', 'ton', 'vall', 'wich', 'win',
        'some', 'smith', 'bridge', 'cope', 'town', 'er', 'don', 'den', 'dell', 'son',
    ]

    def person(self):
        return (WordFactory(language=Common()), WordFactory(language=self))

    def is_valid(self, text):
        for suffix in self.last_vowels:
            if text.endswith(suffix):
                text = text.replace(suffix, '')
                break
        return Common().is_valid(text)
