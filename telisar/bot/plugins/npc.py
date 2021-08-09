from telisar.bot.plugins.base import Plugin, message_parts
from telisar.npc.base import generate_npc, npc_type


class NPC(Plugin):
    """
    Generate NPCs and random traits.

    Supported ancestries:
        dragon, drow, dwarf, elf, halfing, halforc,
        highelf, hightiefling, human, tiefling

    npc [ANCESTRY] ........ Generate an NPC of the specified ancestry or a random ancestry.
    npc names [ANCESTRY] [COUNT].. Generate COUNT randomized NPC names. Defaults to 1 random name.

    """

    command = 'npc'
    help_text = 'Generate randomized NPCs.'

    def run(self, message):
        (_, parts) = message_parts(message)
        if not parts:
            return self.cmd_npc(*parts)
        elif parts[0] == 'names':
            return self.cmd_names(*parts[1:])
        else:
            return self.cmd_npc(*parts[1:])

    def cmd_names(self, ancestry=None, count=1):
        for _ in range(int(count)):
            npc = npc_type(ancestry)
            yield f"{npc.full_name} ({npc.language})"

    def cmd_npc(self, ancestry=None, name=None, pronouns=None, title=None, nickname=None, whereabouts="Unknown",
                STR=None, DEX=None, CON=None, INT=None, WIS=None, CHA=None, randomize=False):
        yield generate_npc(
            ancestry=ancestry,
            names=name.split() if name else [],
            pronouns=pronouns,
            title=title,
            nickname=nickname,
            whereabouts=whereabouts,
            STR=STR,
            DEX=DEX,
            CON=CON,
            INT=INT,
            WIS=WIS,
            CHA=CHA,
            randomize=randomize
        ).character_sheet
