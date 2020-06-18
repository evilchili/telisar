import re

from telisar.npc.npc import BaseNPC


_valid_middle_clusters = re.compile(
    r'^\S?[cc|ht|hty|kd|kl|km|kp|kt|kv|kw|ky|lc|ld|lf|ll|lm|lp|lt|lv|lw|ly|mb|mm|mp|my|' +
    r'nc|nd|ng|ngw|nn|nt|nty|nw|ny|ps|pt|rc|rd|rm|rn|rp|rqu|rr|rs|rt|rty|rw|ry|sc|squ|ss|ts|tt|tw|ty]+\S?$'
)


def _validate_first_syllable(name):

    # anything starting with a vowel is fine
    if name.vowels['pattern'].match(name.as_string[0]):
        return True

    # anything starting with these sequences is fine
    valid = re.compile(r'[ky|ty|ly|ny|nw]')
    if valid.match(name.as_string[:2]):
        return True

    # anything starting with one of these consonants followed by a vowel is fine
    if name.as_string[0] in 'cfhlmnpqrstvwy':
        if name.vowels['pattern'].match(name.as_string[1]):
            return True

    return False


def _validate_last_syllable(name):
    valid = name.vowels['graphemes'] + ['t', 's', 'n', 'l', 'r']
    if name.as_string[-1] not in valid:
        return False
    return True


def _validate_middle_clusters(name):
    last_consonant = ''
    for char in name.as_string:
        if char in name.vowels['graphemes']:
            last_consonant = ''
            continue
        if last_consonant:
            if not _valid_middle_clusters.match(last_consonant + char):
                return False
        last_consonant = char
    return True


class NPC(BaseNPC):
    """
    Random Elf NPCs.
    """
    people = 'elf'
    name_templates = [
        (('c', 'V', 'c'), [0, 1, 2]),
        ('A', [1]),
        (('c', 'V', 'c'), [1, 2, 2]),
    ]

    @staticmethod
    def format_name(names):
        return ' '.join([
            names[0].capitalize(),
            names[1].lower(),
            names[2].capitalize()
        ])

    @staticmethod
    def _validate(name):
        if name.as_string in name.affixes['graphemes']:
            return True
        return (
            _validate_first_syllable(name) and
            _validate_middle_clusters(name) and
            _validate_last_syllable(name)
        )
