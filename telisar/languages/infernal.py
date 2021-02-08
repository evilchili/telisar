from telisar.languages.base import BaseLanguage
import random
import re


class Infernal(BaseLanguage):

    vowels = ['a', 'e', 'i', 'o', 'u']

    consonants = [
        'b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm',
        'n', 'p', 'r', 's', 't', 'v', 'x', 'y', 'z',
        "t'h", "t'j", "t'z", "x't", "x'z", "x'j"
    ]

    syllable_template = ('C', 'V')

    _invalid_sequences = re.compile(
        r'[' + ''.join(vowels) + ']{3}|' +
        r'[' + ''.join(consonants) + ']{4}'
    )

    syllable_weights = [3, 2]

    minimum_length = 1

    def validate_sequence(self, sequence, total_syllables):
        too_short = len(''.join(sequence)) < self.minimum_length
        if too_short:
            return False

        t = ''.join(sequence)

        if self._invalid_sequences.match(t):
            self._logger.debug(f"Invalid sequence: {t}")
            return False
        return True


class Tiefling(Infernal):
    """
    Tiefling names are formed using an infernal root and a few common suffixes.
    """

    nicknames = [
        'eternal',
        'wondrous',
        'luminous',
        'perfect',
        'essential',
        'golden',
        'unfailing',
        'perpetual',
        'infinite',
        'exquisite',
        'sinless',
        'ultimate',
        'flawless',
        'timeless',
        'glorious',
        'absolute',
        'boundless',
        'true',
        'incredible',
        'virtuous',
        'supreme',
        'enchanted',
        'magnificent',
        'superior',
        'spectacular',
        'divine',
    ] + ['' for _ in range(50)]

    def person(self):
        suffix = random.choice([
            'us',
            'ius'
            'to',
            'tro'
            'eus',
            'a',
            'an',
            'is',
        ])
        return [str(self.word()) + suffix]


class HighTiefling(Tiefling):
    """
    "High" Tieflings revere their bloodlines and take their lineage as part of their name.
    """

    nicknames = []

    def person(self):
        bloodline = random.choice([
            'Asmodeus',
            'Baalzebul',
            'Rimmon',
            'Dispater',
            'Fierna',
            'Glasya',
            'Levistus',
            'Mammon',
            'Mephistopheles',
            'Zariel',
        ])
        return [bloodline] + super().person()
