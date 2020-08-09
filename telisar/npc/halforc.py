from telisar.languages import orcish
from telisar.npc.base import BaseNPC


class NPC(BaseNPC):

    language = orcish.HalfOrcPerson()

    @property
    def full_name(self):
        return ' '.join([str(x).capitalize() for x in self.language.person()])
