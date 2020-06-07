import dice

from telisar.bot.plugins.base import Plugin, message_parts


class Roll(Plugin):
    """
    A dice roller. Because you can never have too many dice rollers.

    roll XdY [+Z]....Roll X Y-sided dice where 0 < X,Y < 100. Add (or substract) Z if specified.

    The full 'roll' syntax is anything supported by python-dice; see https://github.com/borntyping/python-dice .
    """
    command = 'roll'
    help_message = "A dice roller."

    def run(self, message):
        (cmd, args) = message_parts(message)

        # roll, if the request is sane.
        try:
            (count, sides) = args[0].split('d', 1)
            if int(count) > 100 or int(sides) > 100:
                results = None
            else:
                results = dice.roll(args[0])
        except (ValueError, dice.exceptions.DiceFatalException, dice.exceptions.DiceException):
            results = None

        if not results:
            return ":game_die: {message.author}: Invalid expression."

        # dice.roll() returns either an Integer or a List, because dice.roll() DGAF
        try:
            total = sum(results)
        except TypeError:
            return f":game_die: {message.author}: {results}"

        # Add the modifier, if there is one
        try:
            modifier = ''.join(args[1:])
            total += int(modifier)
        except (IndexError, TypeError, ValueError):
            modifier = ''

        return f":game_die: {message.author}: {results} {modifier} = {total}"
