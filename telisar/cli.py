from telisar.bot import hammer
from telisar.reckoning import calendar, campaign
from telisar import crypto, bag_of_hoarding
from telisar.npc.base import generate_npc, npc_type

from importlib import import_module

import os
import random
import dotenv
import logging
import fire


dotenv.load_dotenv()

logging.basicConfig(level=logging.WARN)


class CLI:

    def calendar(self):
        """
        Telisar calendaring tools.
        """
        return calendar.Calendar()

    def timeline(self):
        """
        The Noobhammer Chronicles campaign timeline.
        """
        datafile = os.path.expanduser(os.path.expandvars(os.getenv('TIMELINE_DATAFILE')))
        return campaign.Timeline(datafile)

    def hoard(self, count=1):
        """
        Retrieve 1 or more random items from Whisper's Bag of Hoarding.
        """
        for item in [bag_of_hoarding.HoardItem() for i in range(int(count))]:
            print(str(item))

    def npc(self, ancestry=None, name=None, pronouns=None, title=None, nickname=None, whereabouts="Unknown",
            STR=None, DEX=None, CON=None, INT=None, WIS=None, CHA=None, randomize=False):
        """
        Generate a basic NPC.
        """
        return generate_npc(
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

    def names(self, ancestry=None, count=1):
        for _ in range(count):
            print(npc_type(ancestry)().full_name)

    def text(self, language='common', words=50):
        try:
            module = import_module(f'telisar.languages.{language}')
            lang = getattr(module, language.capitalize())()
        except AttributeError:
            print(f'Unsupported Language: {language}.')
            return

        phrases = []
        phrase = []
        for word in [lang.word() for _ in range(words)]:
            phrase.append(str(word))
            if len(phrase) >= random.randint(1, 12):
                phrases.append(' '.join(phrase))
                phrase = []
        if phrase:
            phrases.append(' '.join(phrase))

        paragraph = phrases[0].capitalize()
        for phrase in phrases[1:]:
            if random.choice([0, 0, 1]):
                paragraph = paragraph + random.choice('?!.') + ' ' + phrase.capitalize()
            else:
                paragraph = paragraph + ', ' + phrase
        print(f"{paragraph}.")

    def cipher(self):
        return crypto.Cipher()

    def bot(self):
        """
        Hammer the discord bot.
        """
        print("Starting Discord bot; CTRL+C to shut down cleanly.")
        client = hammer.Hammer()
        client.run()
        print("\nBot shut down. Goodbye.")


if __name__ == '__main__':
    fire.Fire(CLI())
