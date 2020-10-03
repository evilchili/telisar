from importlib import import_module
from telisar.npc import traits
import os
import glob
import random
import dice
import textwrap


_available_npc_types = {}


def a_or_an(s):
    return 'an' if s[0] in 'aeiouh' else 'a'


class BaseNPC:
    """
    The base class for NPCs.
    """

    # define this on your subclass
    language = None

    _names = []

    def __init__(self, names=[], title=None, pronouns=None, nickname=None, whereabouts='Unknown', randomize=False,
                 STR=None, DEX=None, CON=None, INT=None, WIS=None, CHA=None):

        # identity
        self._names = []
        self._pronouns = pronouns
        self._nickname = nickname
        self._title = title

        self._whereabouts = whereabouts

        # appearance
        self._eyes = None
        self._hair = None
        self._face = None
        self._body = None
        self._nose = None
        self._lips = None
        self._teeth = None
        self._skin_tone = None
        self._skin_color = None
        self._facial_hair = None
        self._facial_structure = None
        self._eyebrows = None
        self._age = None
        self._voice = None

        # character
        self._flaw = None
        self._goal = None
        self._personality = None

        stats = (10, 10, 10, 10, 10, 10)
        if randomize:
            stats = self._roll_stats()
        self.STR = STR if STR else stats[0]
        self.DEX = DEX if DEX else stats[1]
        self.CON = CON if DEX else stats[2]
        self.INT = INT if DEX else stats[3]
        self.WIS = WIS if DEX else stats[4]
        self.CHA = CHA if DEX else stats[5]

        self._HP = None

    def _roll_stats(self):
        stats = [15, 14, 13, 12, 10, 8]
        random.shuffle(stats)
        r = random.random()
        if r < 0.3:
            i = random.choice(range(len(stats)))
            stats[i] += (random.choice([-1, 1]) * random.randint(1, 3))
        return stats

    @property
    def HP(self):
        if not self._HP:
            self._HP = str(sum(dice.roll('2d8')) + 2) + ' (2d8+2)'
        return self._HP

    @property
    def names(self):
        if not self._names:
            self._names = [str(x) for x in self.language.person()]
        return self._names

    @property
    def full_name(self):
        name = ' '.join([n.capitalize() for n in self.names])
        if self.title:
            name = self.title.capitalize() + ' ' + name
        if self.nickname:
            name = f'{name} "{self.nickname}"'
        return name

    @property
    def pronouns(self):
        if not self._pronouns:
            self._pronouns = random.choice([
                'he/him',
                'she/her',
                'they/they',
            ])
        return self._pronouns

    @property
    def title(self):
        return self._title

    @property
    def nickname(self):
        return self._nickname

    @property
    def whereabouts(self):
        return self._whereabouts

    @property
    def flaw(self):
        if not self._flaw:
            self._flaw = random.choice(traits.flaws)
        return self._flaw

    @property
    def goal(self):
        if not self._goal:
            self._goal = random.choice(traits.goals)
        return self._goal

    @property
    def personality(self):
        if not self._personality:
            self._personality = ', '.join([
                random.choice(traits.personality),
                random.choice(traits.personality),
                random.choice(traits.personality),
            ])
        return self._personality

    @property
    def eyes(self):
        if not self._eyes:
            self._eyes = ', '.join([random.choice(traits.eye_shape), random.choice(traits.eye_color)])
        return self._eyes

    @property
    def skin_color(self):
        if not self._skin_color:
            self._skin_color = random.choice(traits.skin_color)
        return self._skin_color

    @property
    def skin_tone(self):
        if not self._skin_tone:
            self._skin_tone = random.choice(traits.skin_tone)
        return self._skin_tone

    @property
    def hair(self):
        if not self._hair:
            self._hair = ' '.join([random.choice(traits.hair_style), random.choice(traits.hair_color)])
        return self._hair

    @property
    def face(self):
        if not self._face:
            self._face = random.choice(traits.face)
        return self._face

    @property
    def facial_structure(self):
        if not self._facial_structure:
            self._facial_structure = random.choice(traits.facial_structure)
        return self._facial_structure

    @property
    def lips(self):
        if not self._lips:
            self._lips = random.choice(traits.lips)
        return self._lips

    @property
    def teeth(self):
        if not self._teeth:
            self._teeth = random.choice(traits.teeth)
        return self._teeth

    @property
    def nose(self):
        if not self._nose:
            self._nose = random.choice(traits.nose)
        return self._nose

    @property
    def eyebrows(self):
        if not self._eyebrows:
            self._eyebrows = random.choice(traits.eyebrows)
        return self._eyebrows

    @property
    def facial_hair(self):
        if not self._facial_hair:
            self._facial_hair = random.choice(traits.facial_hair)
        return self._facial_hair

    @property
    def body(self):
        if not self._body:
            self._body = random.choice(traits.body)
        return self._body

    @property
    def age(self):
        if not self._age:
            self._age = random.choice(traits.age)
        return self._age

    @property
    def voice(self):
        if not self._voice:
            self._voice = random.choice(traits.voice)
        return self._voice

    @property
    def description(self):
        desc = (
            f"{self.full_name} ({self.pronouns}) is {a_or_an(self.age)} {self.age}, {self.body} "
            f"{self.ancestry.lower()} with {self.hair} hair, {self.eyes} eyes and {self.skin_color} skin."
        )

        trait = random.choice([
            f'{self.eyebrows} eyebrows',
            self.facial_hair,
            f'a {self.nose} nose',
            f'{self.lips} lips',
            f'{self.teeth} teeth',
            self.facial_structure,
        ])

        desc = desc + ' ' + f"Their face is {self.face}, with {trait}."
        return '\n'.join(textwrap.wrap(desc, width=120))

    @property
    def character_sheet(self):
        return f"""\

{self.description}

Physical Traits:

Face:  {self.face}, {self.eyebrows} eyebrows, {self.nose} nose, {self.lips} lips,
       {self.teeth} teeth, {self.facial_hair}
Eyes:  {self.eyes}
Skin:  {self.skin_tone}, {self.skin_color}
Hair:  {self.hair}
Body:  {self.body}
Voice: {self.voice}

Stats:
    AC  10
    HP  {self.HP}
    STR {self.STR}
    DEX {self.DEX}
    CON {self.CON}
    INT {self.INT}
    WIS {self.WIS}
    CHA {self.CHA}

Details:

Personality: {self.personality}
Flaw:        {self.flaw}
Goal:        {self.goal}

Whereabouts: {self.whereabouts}

"""

    def __repr__(self):
        return f"{self.full_name}"


def available_npc_types():
    """
    Load all available NPC submodules and return a dictionary keyed by module name.
    """
    if not _available_npc_types:
        for filename in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), '*.py')):
            module_name = os.path.basename(filename)[:-3]
            if module_name not in ['base', '__init__', 'traits']:
                _available_npc_types[module_name] = import_module(f'telisar.npc.{module_name}').NPC
    return _available_npc_types


def npc_type(ancestry=None):
    """
    Return the NPC class for the specified ancestry, or a random one.
    """
    if not ancestry:
        non_humans = [x for x in available_npc_types() if x != 'human']
        if random.random() <= 0.7:
            ancestry = 'human'
        else:
            ancestry = random.choice(non_humans)
    return available_npc_types()[ancestry]


def generate_npc(ancestry=None, names=[], pronouns=None, title=None, nickname=None, whereabouts="Unknown",
                 STR=0, DEX=0, CON=0, INT=0, WIS=0, CHA=0, randomize=False):
    """
    Return a randomized NPC. Any supplied keyword parameters will override the generated values.

    By default, NPC stats are all 10 (+0). If randomize is True, the NPC will be given random stats from the standard
    distribution, but overrides will still take precedence.
    """
    return npc_type(ancestry)(
        names=names,
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
     )
