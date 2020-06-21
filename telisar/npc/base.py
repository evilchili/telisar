class BaseNPC:
    """
    The base class for NPCs.
    """

    # define this on your subclass
    language = None

    _names = []

    def __init__(self, names=[]):
        self._names = []

    @property
    def names(self):
        if not self._names:
            self._names = self.language.word()
        return self._names

    @property
    def full_name(self):
        return ' '.join([n.capitalize() for n in self.names])

    def __repr__(self):
        return self.full_name
