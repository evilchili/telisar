import re

from telisar.languages.base import BaseLanguage, LanguageException


class Elven(BaseLanguage):
    """
    Phonetics for the Elven language in Telisar. Loosely based on Tolkein's Quenya language, but with character tweaks
    and naming conventions following Twirrim's conventions in-game.
    """

    _vowels = ['a', 'e', 'i', 'o', 'u']
    _consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'l', 'k', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'y', 'z']
    _affixes = ['am', 'an', 'al']

    _valid_middle_clusters = re.compile(
        r'^\S?[cc|ht|hty|kd|kl|km|kp|kt|kv|kw|ky|lc|ld|lf|ll|lm|lp|lt|lv|lw|ly|mb|mm|mp|my|' +
        r'nc|nd|ng|ngw|nn|nt|nty|nw|ny|ps|pt|rc|rd|rm|rn|rp|rqu|rr|rs|rt|rty|rw|ry|sc|squ|ss|ts|tt|tw|ty]+\S?$'
    )

    def is_valid_word(self, word):
        """
        Override the default word validator to invoke our custom validation.
        """
        word = word.lower()

        # elven affixes are words
        try:
            if self.is_valid_affix(word):
                return True
        except LanguageException:
            pass

        try:
            return (
                self._validate_first_syllable(word) and
                self._validate_middle_clusters(word) and
                self._validate_last_syllable(word)
            )
        except LanguageException:
            self._logger.debug(f"Invalid word: {word}", exc_info=True)
        return False

    def person_name(self):
        """
        Use custom syllable templtates for names. The elves of Telisar typically two names, a given name and a surname.
        The surname is always preceded by an affix (am, an, or al); in the First Age surnames were simply the location
        of a person's birth (during adolescence), or wherever they found renown (in adulthood).

        Returns:
            list: a list of names consisting of the given name, the affix, and the surname.
        """
        templates = [
            (('c', 'V', 'c', 'v'), [1, 1]),
            ('A', [1])
        ]
        names = []
        for (template, weights) in templates:
            names.append(self.word(template, weights))
        names.append(self.place_name())
        return names

    def place_name(self):
        """
        Place names always have two or three syllables.
        """
        return self.word(('c', 'V', 'v', 'c'), [1, 2])

    def _validate_first_syllable(self, word):

        if len(word) < 3:
            return False

        # anything starting with a vowel is fine
        try:
            if self.is_valid_vowel(word[0]):
                return True
        except LanguageException:
            pass

        # anything starting with these sequences is fine
        valid = re.compile(r'[glmnrstv][aeiouy]')
        if valid.match(word[:2]):
            return True

        return False

    def _validate_last_syllable(self, word):
        if word[-1] not in ['t', 's', 'n', 'l', 'r', 'd', 'a']:
            return False
        return True

    def _validate_middle_clusters(self, word):
        last_consonant = ''
        for char in word:
            if char in [v.char for v in self.vowels]:
                last_consonant = ''
                continue
            if last_consonant:
                if not self._valid_middle_clusters.match(last_consonant + char):
                    print(f"word {word} contains invalid sequence: {last_consonant}{char}")
                    return False
            last_consonant = char
        return True
