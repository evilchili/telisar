import os
import dotenv
import telisar.bot.hammer as _hammer
import telisar.reckoning.calendar as _calendar
import telisar.reckoning.campaign as _campaign
import telisar.bag_of_hoarding as _hoard

dotenv.load_dotenv()


def calendar():
    """
    Telisar calendaring tools.
    """
    return _calendar.Calendar()


def timeline():
    """
    The Noobhammer Chronicles campaign timeline.
    """
    datafile = os.path.expanduser(os.path.expandvars(os.getenv('TIMELINE_DATAFILE')))
    return _campaign.Timeline(datafile)


def hoard(count=1):
    """
    Retrieve 1 or more random items from Whisper's Bag of Hoarding.
    """
    for item in [_hoard.HoardItem(os.environ.get(_hoard.DATA_PATH_VARIABLE)) for i in range(int(count))]:
        print(str(item))


def bot():
    """
    Hammer the discord bot.
    """
    print("Starting Discord bot; CTRL+C to shut down cleanly.")
    client = _hammer.Hammer()
    client.run()
    print("\nBot shut down. Goodbye.")
