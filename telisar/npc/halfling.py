import random

from telisar.languages import halfling
from telisar.npc.base import BaseNPC


class NPC(BaseNPC):

    ancestry = 'Halfling'
    language = halfling.Halfling()
