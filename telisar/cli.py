import os
import dotenv
import telisar.bot.hammer as _hammer
import telisar.reckoning.calendar as _calendar
import telisar.reckoning.campaign as _campaign

dotenv.load_dotenv()


def calendar():
    """
    Telisar calendaring tools.
    """
    return _calendar.Calendar()


def timeline():
    datafile = os.path.expanduser(os.path.expandvars(os.getenv('TIMELINE_DATAFILE')))
    return _campaign.Timeline(datafile)


def bot():
    """
    Hammer the discord bot.
    """
    print("Starting Discord bot...")
    client = _hammer.Hammer()
    client.run()
