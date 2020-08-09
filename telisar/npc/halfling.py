import random

from telisar.languages import halfling
from telisar.npc.base import BaseNPC


class NPC(BaseNPC):

    language = halfling.Halfling()

    @property
    def full_name(self):
         true_name = ' '.join([str(x).capitalize() for x in self.language.person()])
         return f"{true_name} ({self.nickname})"

    @property
    def nickname(self):
        return random.choice(self.language.nicknames).capitalize()
