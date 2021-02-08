from telisar.languages import draconic
from telisar.npc.base import BaseNPC, a_or_an
from telisar.npc import traits
import textwrap
import random


class NPC(BaseNPC):

    ancestry = 'Dragon'
    language = draconic.Dragon()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tail = None
        self._horns = None
        self._fangs = None
        self._wings = None

    @property
    def nickname(self):
        if not self._nickname:
            self._nickname = "the " + random.choice(traits.personality)
        return self._nickname

    @property
    def age(self):
        if not self._age:
            self._age = random.choice([
                'wyrmling',
                'young',
                'adult',
                'ancient',
            ])
        return self._age

    @property
    def pronouns(self):
        if not self._pronouns:
            self._pronouns = 'they/they'
        return self._pronouns

    @property
    def skin_color(self):
        if not self._skin_color:
            self._skin_color = random.choice([
                'red',
                'white',
                'green',
                'black',
                'blue',
                'brass',
                'bronze',
                'copper',
                'silver',
                'gold',
            ])
        return self._skin_color

    @property
    def description(self):
        trait = random.choice([
            f'{self.eyes} eyes',
            f'{self.tail} tail',
            f'{self.eyebrows} eyebrows',
            f'{self.teeth} fangs',
            self.facial_structure,
        ])
        return (
            f"{self.full_name} ({self.pronouns}) is {a_or_an(self.age)} {self.age} {self.skin_color} "
            f"{self.ancestry.lower()} with {a_or_an(self.nose)} {self.nose} snout, {self.body} body and {trait}."
        )

    @property
    def character_sheet(self):
        desc = '\n'.join(textwrap.wrap(self.description, width=120))
        return f"""\

{desc}

Physical Traits:

Face:  {self.face}, {self.eyebrows} eyebrows, {self.nose} nose, {self.lips} lips,
       {self.teeth} teeth, {self.facial_hair}
Eyes:  {self.eyes}
Skin:  {self.skin_tone}, {self.skin_color}
Hair:  {self.hair}
Body:  {self.body}
Tail:  {self.tail}
Voice: {self.voice}

Details:

Personality: {self.personality}
Flaw:        {self.flaw}
Goal:        {self.goal}

Whereabouts: {self.whereabouts}

"""
