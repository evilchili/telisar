from telisar.bot.plugins.base import Plugin, message_parts
from telisar.npc.base import generate_npc, npc_type


class NPC(Plugin):
    """
    Generate NPCs and random traits.

    Supported ancestries:
        dragon, drow, dwarf, elf, halfing, halforc,
        highelf, hightiefling, human, tiefling

    npc [ANCESTRY] [ROLLSTATS] ........ Generate an NPC. Defaults to random ancestry. If ROLSTATS=True, generate stats.
    npc names [ANCESTRY] [COUNT]....... Generate COUNT randomized NPC names. Defaults to 1 random name.

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
            return self.cmd_npc(*parts)

    def cmd_names(self, ancestry=None, count=1):
        for _ in range(int(count)):
            npc = npc_type(ancestry)()
            yield npc.full_name

    def cmd_npc(self, ancestry=None, randomize=False):
        yield generate_npc(
            ancestry=ancestry,
            whereabouts='Unknown',
            randomize=randomize
        ).character_sheet
