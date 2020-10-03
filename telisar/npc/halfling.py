import random

from telisar.languages import halfling
from telisar.npc.base import BaseNPC


class NPC(BaseNPC):

    ancestry = 'Halfling'
    language = halfling.Halfling()

    @property
    def nickname(self):
        if not self._nickname:
            self._nickname = random.choice(self.language.nicknames).capitalize()
        return self._nickname
