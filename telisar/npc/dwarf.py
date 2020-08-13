from telisar.languages import dwarvish
from telisar.npc.base import BaseNPC


class NPC(BaseNPC):

    language = dwarvish.Dwarvish()

    @property
    def full_name(self):
        return ' '.join([str(x).capitalize() for x in self.language.person()])
