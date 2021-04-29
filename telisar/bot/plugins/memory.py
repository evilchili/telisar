from telisar.bot.plugins.base import Plugin, message_parts
import os
import json

MEMORY_VARIABLE = 'MEMORY_FILENAME'


class Memory(Plugin):
    """
    Remember definitions.

    remember TERM = DEFINITION .. Remember TERM's DEFINITION.
    what [is] TERM .............. Recall the definition of TERM.
    TERM? ....................... Same as "what is"
    """
    command = 'remember'
    help_text = 'Remember definitions.'
    receive_all = True

    def __init__(self):
        self._memory_file = None
        self._memory = {}
        super().__init__()

    def check_config(self):
        self._memory_file = os.environ.get(MEMORY_VARIABLE, None)
        if not self._memory_file:
            self.logger.error(f"{MEMORY_VARIABLE} not defined.")
            return False
        return self.load_memory()

    def load_memory(self):
        try:
            with open(self._memory_file) as f:
                self._memory = json.load(f)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to load memory: {e}")
            return False
        return True

    def write_memory(self):
        with open(self._memory_file, 'wb') as f:
            f.write(json.dumps(self._memory, indent=2).encode())
        return True

    def cmd_remember(self, author, term, definition):
        """
        Remember a definition.
        """
        term = term.strip().lower()
        self._memory[term] = (author.name, definition.strip())
        self.write_memory()
        yield f"Okay, I'll remember {author.name} told me '{term}' is {definition}."

    def cmd_recall(self, term):
        """
        Recall a definition.
        """
        try:
            (author, definition) = self._memory[term.strip().lower()]
            yield f"I remember {author} told me **{term}** is {definition}"
        except KeyError:
            yield f"I don't know what {term} is."

    def run(self, message):
        (_, parts) = message_parts(message)

        self.logger.debug(_)
        self.logger.debug(parts)

        if _.lower() == 'what':
            if parts[0].lower() == 'is':
                parts = parts[1:]
            return self.cmd_recall(' '.join(parts))

        if _[-1][-1] == '?':
            return self.cmd_recall(f"{_} {' '.join(parts)}".strip()[:-1])

        if '=' in parts:
            (term, definition) = ' '.join(parts).split('=', 1)
            return self.cmd_remember(message.author, term, definition)
