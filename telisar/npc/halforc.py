from telisar.languages import orcish
from telisar.npc.base import BaseNPC


class NPC(BaseNPC):

    language = orcish.HalfOrcPerson()

    @property
    def full_name(self):
        names = [str(x) for x in self.language.person()]
        return ' '.join(names)
