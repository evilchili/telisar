from telisar.languages import common
from telisar.npc.base import BaseNPC


class NPC(BaseNPC):

    language = common.Common()

    @property
    def full_name(self):
        return ' '.join([str(x).capitalize() for x in self.language.person()])
