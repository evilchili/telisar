from telisar.bot.plugins.base import Plugin, message_parts
from telisar.npc.base import generate_npc, npc_type


class NPC(Plugin):
    """
    Generate NPCs and random traits.

    npc [ANCESTRY] ........ Generate an NPC of the specified ancestry.
    npc names [ANCESTRY] .. Generate randomized NPC names.

    """

    command = 'npc'
    help_text = 'Generate randomized NPCs.'

    def run(self, message):
        (_, parts) = message_parts(message)
        if not parts:
            return self.cmd_npc(*parts)
        try:
            handler = getattr(self, f"cmd_{parts[0].lower()}")
        except AttributeError:
            self.logger.debug(f"Ignoring unsupported command: {parts[0]}")
            return
        return handler(*parts[1:])

    def cmd_names(self, ancestry=None, count=1):
        for _ in range(count):
            yield npc_type(ancestry)().full_name

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
