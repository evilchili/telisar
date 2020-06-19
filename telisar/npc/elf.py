from telisar.languages import elven
from telisar.npc.base import BaseNPC


class NPC(BaseNPC):

    language = elven.Elven()

    @property
    def full_name(self):
        return ' '.join([
            self.names[0].capitalize(),
            self.names[1].lower(),
            self.names[2].capitalize()
        ])
