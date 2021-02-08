from telisar.languages import infernal
from telisar.npc import tiefling


class NPC(tiefling.NPC):
    language = infernal.HighTiefling()
