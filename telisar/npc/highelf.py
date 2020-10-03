from telisar.languages import elven
from telisar.npc.base import BaseNPC


class NPC(BaseNPC):

    ancestry = 'Elf'
    language = elven.HighElvenPerson()

    @property
    def full_name(self):
        return ' '.join([
            str(self.names[0]).capitalize(),
            str(self.names[1]).lower(),
            str(self.names[2]).capitalize()
        ])
