from telisar.languages import infernal
from telisar.npc.base import BaseNPC
import random


class NPC(BaseNPC):
    ancestry = 'Tiefling'
    language = infernal.Tiefling()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tail = None
        self._horns = None

    @property
    def skin_color(self):
        if not self._skin_color:
            self._skin_color = random.choice([
                'reddish',
                'white',
                'green',
                'black',
                'blue',
                'brassy',
                'bronze',
                'coppery',
                'silvery',
                'gold',
            ])
        return self._skin_color

    @property
    def full_name(self):
        name = ' '.join([n.capitalize() for n in self.names])
        if self.title:
            name = self.title.capitalize() + ' ' + name
        if self.nickname:
            name = name + ' ' + self.nickname.capitalize()
        return name
