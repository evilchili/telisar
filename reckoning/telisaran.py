"""
Primitives for the Telisaran reckoning of dates and time.
"""
from abc import ABC, abstractmethod
import inspect
import sys
import re


class ReckoningError(Exception):
    pass


class ParseError(ReckoningError):
    pass


class InvalidEraError(ReckoningError):
    pass


class InvalidYearError(ReckoningError):
    pass


class InvalidSeasonError(ReckoningError):
    pass


class InvalidSpanError(ReckoningError):
    pass


class InvalidDayError(ReckoningError):
    pass


class InvalidHourError(ReckoningError):
    pass


class InvalidMinuteError(ReckoningError):
    pass


class InvalidSecondError(ReckoningError):
    pass


class InvalidDateError(ReckoningError):
    pass


class MissingSeasonError(ReckoningError):
    pass


def _suffix(n):
    if n == 1:
        return 'st'
    elif n == 2:
        return 'nd'
    elif n == 3:
        return 'rd'
    else:
        return 'th'


class DateObject(ABC):  # pragma: no cover
    """
    Base class for all date components. This ABC implements basic arithmetic operator support for
    all DateObjects as integer seconds since the beginning of time. If the current instance has a
    from_seconds() method, it will be called with the result of the calculation, otherwise the
    integer seconds will be returned.

    Subclasseres must define the number, as_seconds and length_in_seconds attributes.

    Attribtues:
        number (int): The numeric index of the object in its parent group
        as_seconds (int): The component object expressed as seconds since the beginning of time.
        length_in_seconds (int): The number of seconds in a single object.
    """

    @property
    @abstractmethod
    def number(self):
        pass

    @property
    def as_seconds(self):
        return (self.number - 1) * self.length_in_seconds

    def length_in_seconds(self):
        raise NotImplementedError("Please define the length_in_seconds class attribute.")

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return str(self)

    def __int__(self):
        return self.as_seconds

    def __eq__(self, other):
        return int(self) == int(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __lt__(self, other):
        return not self.__ge__(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        val = int(self) + int(other)
        if hasattr(self.__class__, 'from_seconds'):
            return self.__class__.from_seconds(val)
        else:
            return val

    def __sub__(self, other):
        val = int(self) - int(other)
        if hasattr(self.__class__, 'from_seconds'):
            return self.__class__.from_seconds(val)
        else:
            return val


class datetime(DateObject):
    """
    A date and time on the Telisaran calendar.

    Attributes:
        era (Era): The era component of the date
        year (Year): The year component of the date
        season (Season): The season component of the date
        day (Day): The day component of the date
        hour (Hour): The hour component of the time
        minute (Minute): The minute component of the time
        second (int): The seconds component of the time
        long (str): The long representation of the date and time
        short (str): The short representation of the date and time
        numeric (str): The dotted numeric representation of the date and time
        numeric_date (str): The dotted numeric representation of the date (no time)
        date (str): The shorthand representation of the day and date
        time_long (str): The long form of the time, including names of hours
        time_short (str): The short form of the time
        time (str): Alias of time_short
        as_seconds (int): The date and time expressed in seconds since the beginning of time
        number (int): alias for as_seconds
    """

    def __init__(self, era=1, year=1, season=1, day=1, hour=0, minute=0, second=0):
        """
        Args:
            year (int): The year
            season (int): The season, 1-8
            day (int): The day, 1-45
            era (int): The era, 1-3
        """
        self.era = Era(era)
        self.year = Year(year, era=self.era)
        if season == Year.length_in_seasons + 1:
            self.season = FestivalOfTheHunt(year)
        else:
            self.season = Season(season_of_year=season, year=self.year.year)
        self.day = Day(day, season=self.season)
        self.hour = Hour(hour)
        self.minute = Minute(minute)

        if second < 0 or second > 59:
            raise InvalidSecondError("second {} must be between 0 and 59".format(second))
        self.second = second

    @property
    def long(self):

        if self.season.number == 9:
            template = ("{time} on {day_name}, the {day}{day_suffix} day of the {season}, "
                        "in the year {year} of the {era}")
        else:
            template = ("{time} on {day_name}, the {day}{day_suffix} day of the {season} "
                        "(the {span_day}{span_day_suffix} day of the {span}{span_suffix} span) "
                        "in the year {year} of the {era}")
        return template.format(
            time=self.time_long,
            day_name=self.day.name,
            day=self.day.day_of_season,
            day_suffix=_suffix(self.day.day_of_season),
            season=self.season,
            span_day=self.day.day_of_span,
            span_day_suffix=_suffix(self.day.day_of_span),
            span=self.day.span,
            span_suffix=_suffix(self.day.span),
            year=self.year,
            era=self.era.long
        )

    @property
    def numeric(self):
        return (
            "{0.era.number}.{0.year.number}.{0.season.number}."
            "{0.day.day_of_season:02d}."
            "{0.hour.number:02d}.{0.minute.number:02d}.{0.second:02d}"
        ).format(self)

    @property
    def numeric_date(self):
        return (
            "{0.era.number}.{0.year.number}.{0.season.number}."
            "{0.day.day_of_season:02d}"
        ).format(self)

    @property
    def date(self):
        if self.season.number == 9:
            season = 'H'
        else:
            season = self.season.name[0].upper()

        return "{name}{date}{season}".format(
            name=self.day.name[0].upper(),
            date=self.day.day_of_season,
            season=season,
        )

    @property
    def time_long(self):
        return "{minute}{hour}".format(
            minute="{} past ".format(self.minute) if self.minute != 0 else '',
            hour=self.hour.name
        )

    @property
    def time(self):
        return "{0.hour.number:02d}:{0.minute.number:02d}:{0.second:02d}".format(self)

    @property
    def time_short(self):
        return "{name}, {day}{suffix} of the {season}, {year} {era} {time}".format(
            name=self.day.name,
            day=self.day.day_of_season,
            suffix=_suffix(self.day.day_of_season),
            season=self.season.name,
            year=self.year,
            era=self.era.short,
            time=self.time
        )

    @property
    def short(self):
        return self.time_short

    @property
    def as_seconds(self):
        return sum(map(int, [self.era, self.year, self.season, self.day, self.hour, self.minute, self.second]))

    @property
    def number(self):
        return self.as_seconds

    def __repr__(self):
        return (
            "<Date: era={0.era}, year={0.year}, season={0.season.season_of_year}, "
            "day={0.day.day_of_season}, span={0.day.span}, "
            "hour={0.hour}, minute={0.minute}, second={0.second}>: {0.short}".format(self)
        )

    @classmethod
    def from_expression(cls, expression, now=None, timeline=None):
        return parser(now=now, timeline=timeline).parse(expression)

    @classmethod
    def from_seconds(cls, seconds):
        """
        Return a datetime object corresponding to the given number of seconds since the beginning.
        """
        for (era, years) in enumerate(Era.years):
            if years is None:
                break
            era_length = years * Year.length_in_seconds
            if seconds > era_length:
                seconds -= era_length
            else:
                break

        year = int((seconds) / Year.length_in_seconds)
        y_sec = year * Year.length_in_seconds

        season = int((seconds - y_sec) / Season.length_in_seconds)
        s_sec = season * Season.length_in_seconds

        day = int((seconds - y_sec - s_sec) / Day.length_in_seconds)
        d_sec = day * Day.length_in_seconds

        hour = int((seconds - y_sec - s_sec - d_sec) / Hour.length_in_seconds)
        h_sec = hour * Hour.length_in_seconds

        minute = int((seconds - y_sec - s_sec - d_sec - h_sec) / Minute.length_in_seconds)
        m_sec = minute * Minute.length_in_seconds

        seconds = seconds - y_sec - s_sec - d_sec - h_sec - m_sec

        return cls(
            era=era + 1,
            year=year + 1,
            season=season + 1,
            day=day + 1,
            hour=hour,
            minute=minute,
            second=seconds
        )


class Minute(DateObject):
    """
    A representation of one minute on the Telisaran clock.

    Class Attributes:
        length_in_seconds (int): The length of an hour in seconds

    Attributes:
        minute (int): The minute of the hour (0-59)
        number (int): alias for minute
    """
    length_in_seconds = 60

    def __init__(self, minute):
        if minute < 0 or minute > 59:
            raise InvalidMinuteError("minute {} must be between 0 and 59")
        self.minute = minute

    @property
    def as_seconds(self):
        return self.number * Minute.length_in_seconds

    @property
    def number(self):
        return self.minute


class Hour(DateObject):
    """
    A representation of one hour on the Telisaran clock.

    Class Attributes:
        length_in_seconds (int): The length of an hour in seconds

    Instance Attributes:
        hour (int): The hour of the day (0-23)
        number (int): alias for hour
    """
    length_in_seconds = 60 * Minute.length_in_seconds

    names = {
        '0': "Black Hour",
        '6': "Soul's Hour",
        '12': "Sun's Hour",
        '18': "Grey Hour",
    }

    def __init__(self, hour):
        if hour < 0 or hour > 23:
            raise InvalidHourError("hour {} must be between 0 and 23")
        self.hour = hour

    @property
    def as_seconds(self):
        return self.number * Hour.length_in_seconds

    @property
    def number(self):
        return self.hour

    @property
    def name(self):
        if str(self) in Hour.names:
            return Hour.names[str(self)]
        else:
            return "{}{} hour".format(str(self), _suffix(int(self)))


class Day(DateObject):
    """
    A representation of one day on the Telisaran calendar.

    Class Attributes:
        length_in_seconds (int): The length of a day in seconds
        names (list): The names of the days

    Instance Attributes:
        day_of_season (int): The day of the season (1 - 45)
        day_of_span (int): The day of the span  (
        name (str): The name of the day
        season (Season): The Season in which this day occurs
        span (int): The span of the season in which this day falls (1 - 9)
    """
    length_in_seconds = 24 * Hour.length_in_seconds

    names = ['Syfdag', 'Mimdag', 'Wodag', 'Thordag', 'Freydag']

    def __init__(self, day_of_season, season=None):
        """
        Create a Day instance.

        Args:
            day_of_season (int): The day of the season between 1 and 45.
            season (Season): optional, specify a Season instance for this day.
        """
        if day_of_season < 1 or day_of_season > Season.length_in_days:
            raise InvalidDayError("{}: day_of_season must be between 1 and {}".format(
                day_of_season, Season.length_in_days))

        self.day_of_season = day_of_season
        self.season = season

    @property
    def number(self):
        return self.day_of_season

    @property
    def span(self):
        return int((self.day_of_season - 1) / Span.length_in_days) + 1

    @property
    def day_of_span(self):
        return (self.day_of_season - 1) % Span.length_in_days + 1

    @property
    def name(self):
        if self.season.number == 9:
            return self.season.day_names[self.day_of_span - 1]
        else:
            return Day.names[self.day_of_span - 1]

    def __repr__(self):
        return self.name


class Span(DateObject):
    """
    A span (week) of days in a Season.

    Class Attributes:
        length_in_days (int): The number of days in a span.
    """
    length_in_days = len(Day.names)
    length_in_seconds = length_in_days * Day.length_in_seconds

    @property
    def number(self):
        return 1


class Season(DateObject):
    """
    A season (month) of days in a Telisaran year.

    Class Attributes:
        names (list): The names of the seasons
        length_in_spans (int): The number of spans in a season
        length_in_days (int): The number of days in a season

    Instance Attributes:
        name (str): The name of the season
        season_of_year (int): The season of the year, between 1 and 8.
        days (list): A list of Day objects for every day in the season
        year (int): The year in which this season falls.
    """
    names = ['Fox', 'Owl', 'Wolf', 'Eagle', 'Shark', 'Lion', 'Raven', 'Bear']
    length_in_spans = 9
    length_in_days = length_in_spans * Span.length_in_days
    length_in_seconds = length_in_days * Day.length_in_seconds

    def __init__(self, season_of_year, year):
        if season_of_year < 1 or season_of_year > len(Season.names):
            raise InvalidSeasonError("season_of_year {} must be between 1 and {}".format(
                season_of_year, len(Season.names)))
        self.season_of_year = season_of_year
        self.year = year

        self._days = []

    @property
    def number(self):
        return self.season_of_year

    @property
    def days(self):
        if not self._days:
            for i in range(1, Season.length_in_days + 1):
                self._days.append(Day(i, season=self))
        return self._days

    @property
    def name(self):
        return Season.names[self.season_of_year - 1]

    def __int__(self):
        return (self.season_of_year - 1) * self.length_in_seconds

    def __str__(self):
        return "Season of the {}".format(self.name)


class FestivalOfTheHunt(Season):
    """
    The 9th season, which only has 5 days, occurring at the end of each year.

    Class Attributes:
        day_names (list): The names of the days in this season
        length_in_spans (int): the length of the festival in spans
        length_in_days (int): The length of the festival in days
        length_in_seconds (int): The length of the festival in seconds

    Instance Attributes:
        season_of_year (int): The season of the year (9)
        days (list): A list of Day objects for every day in the season
        name (str): The name of this special season
        year (Year): The year in which this festival falls
    """
    day_names = [
        "Syf's Hunt",
        "Mimir's Hunt",
        "Woden's Hunt",
        "Thorus's Hunt",
        "Freya's Hunt"
    ]
    length_in_spans = 1
    length_in_days = 5
    length_in_seconds = length_in_days * Day.length_in_seconds

    def __init__(self, year):
        self.season_of_year = 9
        self.year = year
        self._days = []

    @property
    def name(self):
        return "Festival Of The Hunt"

    def __int__(self):
        return (self.season_of_year - 1) * Season.length_in_seconds

    def __str__(self):
        return "the {}".format(self.name)


class Year(DateObject):
    """
    A year on the Telisaran calendar.

    Class Attributes:
        length_in_seasons (int): The length of a year in seasons
        length_in_spans (int): The length of a year in spans
        length_in_days (int): The length of a year in days
        length_in_seconds (int): The length of a year in seconds

    Instance Attributes:
        era (Era): The era
        year (Year): The year
        seasons (list): The seasons in the year
        number (int): Alias of year
    """

    # precompute some length properties. Note that every year has one extra span, the Festival Of
    # The Hunt, which falls between the last span of the Bear and the first span of the Fox.
    length_in_seasons = len(Season.names)
    length_in_spans = (length_in_seasons * Season.length_in_spans) + 1
    length_in_days = length_in_spans * Span.length_in_days
    length_in_seconds = length_in_days * Day.length_in_seconds

    def __init__(self, year, era):
        """
        Instantiate a Year object

        Args:
            year (int): The year of the era.
            era (int): The era
        """
        self.era = era
        if year < 1:
            raise InvalidYearError("Years must be greater than 1.")
        if self.era.end and year > self.era.end:
            raise InvalidYearError("The {} ended in {}".format(self.era.long, self.era.end))
        self.year = year
        self.seasons = [Season(i, self) for i in range(1, Year.length_in_seasons + 1)]
        self.seasons.append(FestivalOfTheHunt(self))

    @property
    def number(self):
        return self.year


class Era(DateObject):
    """
    An age of years, by Telisaran reckoning.

    Class Attributes:
        long_names (list): The long names of the eras
        shot_names (list): The abbreviated names of the eras
        lenth_in_seconds (int): The length of an era, in seconds

    Instance Attributes:
        era (int): The number of the era (1-3)
        end (int): The last year of the era
        short (str): The short name of this era
        long (str): The long name of this era
        number (int): Alias for era

    """
    long_names = ['Ancient Era', 'Old Era', 'Modern Era']
    short_names = ['AE', 'OE', 'ME']
    years = [20000, 10000, None]

    def __init__(self, era, end=None):
        """
        Args:
            era (int): The number of the era; must be between 1 and 3.
            end (year): The last year of the era
        """
        if era < 1 or era > len(Era.long_names):
            raise InvalidEraError("{}: Eras must be between 0 and {}".format(era, len(Era.long_names)))
        self.era = era
        self.end = Era.years[self.era - 1]
        self.length_in_seconds = sum(Era.years[:self.era - 1]) * Year.length_in_seconds

    @property
    def short(self):
        return Era.short_names[self.era - 1]

    @property
    def long(self):
        return Era.long_names[self.era - 1]

    @property
    def number(self):
        return self.era

    def __int__(self):
        return self.length_in_seconds

    def __repr__(self):
        return self.long


class parser:
    """
    A lexical date expression parser that can understand various relative dates. Some examples:

    2 days before 3.3206.3.36
    11 spans later than now
    yesterday
    tomorrow
    2 days after tomorrow
    11 spans later than now
    yesterday
    1000 years ago
    on 1.193.1.1
    at 2.4839.7.22

    If initialized with a timeline, the parser will also support references to events:

    36 hours before campaign start
    11 spans after the party returns from the feywild

    Class Attributes:

        future_modifiers (list): list of phrases that indicate a positive (future) date
        past_modifiers (list): list of phrases that indicate a negative (past) date
        patterns (list): A list of regular expression objects that will be used, in order, to parse
            the date expressions

    Instance Attributes:
        now (int): the date relative to which dates will be calculated, in seconds.
        timeline (dict): A dictionary of event datetimes

    """

    future_modifiers = [
        'from',
        'after',
        'later than',
    ]

    past_modifiers = [
        'before',
        'ago',
        'earlier than',
        'prior to',
    ]

    patterns = [
        # <value> <unit> <modifier> <start>
        re.compile(
            r'(?P<value>\d+)\s*' +
            r'(?P<unit>\w+)\s+' +
            r'(?P<modifier>{}|{})'.format(
                '|'.join(future_modifiers),
                '|'.join(past_modifiers)) +
            r'(?P<start>.*)',
        ),

        # at <start>
        re.compile(r'(?P<modifier>at)\s+(?P<start>.*)'),
    ]

    def __init__(self, now=None, timeline={}):
        """
        Constructor

        Args:
            now (datetime): the date against which calculate the relative date
            timeline (dict): a dictionary of event datetimes keyed by description
        """
        self.timeline = timeline

        if not now:
            self.now = today.as_seconds
        else:
            try:
                self.now = self.timeline[str(now)].as_seconds
            except KeyError:
                self.now = int(now)

    def parse(self, expression):
        """
        Parse an expression and return a datetime object computed relative to 'now'.

        Args:
            expression (str): The expression to parse.

        Returns:
            datetime: A datetime object
        """
        for pattern in parser.patterns:
            m = pattern.match(expression)
            if m:
                return datetime.from_seconds(self.calculate_date(**m.groupdict()))
        raise ParseError("Could not parse expression '{}' using any pattern".format(
            expression))

    def _parse_value(self, value, unit):
        """
        Convert a value into integer seconds.

        Args:
            value (int): the value to convert (eg. "2", "37")
            unit (str): The units to convert to seconds (eg. "Days", "Year")

        Returns:
            int: The integer seconds of value * units, or 0 if either of value or unit is None
        """
        if None not in (value, unit):
            return int(value) * self.get_unit_class(unit).length_in_seconds
        return 0

    def _parse_start(self, expression):
        """
        Convert a starting time expression to a datetime object. The expression can be one of:

        - a date in numeric format (eg. "3.3206.12.17");
        - a datetime instance defined in this module (eg. "yesterday", "tomorrow")
        - a member of the timeline dictionary

        If start is False, the parser's 'now' will be used.

        Args:
            expression (str): The expression to convert to a datetime object

        Returns:
            datetime: The datetime object

        Raises:
            ParseError: If the sub-expression cannot be parsed
        """

        # if there is no start, use 'now', ie, whatever the parser was seeded with for now
        if not expression:
            return self.now

        # if start is a member of the timeline, use the date associated with that event
        if expression in self.timeline:
            return self.timeline[expression]

        # the start might be a datetime instane defined by this module ('yesterday', 'today', etc)
        try:
            return [
                i for i in inspect.getmembers(sys.modules[__name__]) if isinstance(i[1], datetime)
            ][0][1]
        except IndexError:
            pass

        # the start might be a numeric date string
        try:
            return datetime(*(map(int, expression.split('.'))))
        except ValueError:
            raise ParseError("Unable to parse date exprssion {}".format(expression))

    def calculate_date(self, modifier, start='', value=None, unit=None):
        """
        Calculate a date by parsing a modifier sub-expression, possibly with a value and unit,
        and applying it to the starting date.

        Args:
            modifier (str): A string specifying what kind of calculation to make; must be a member
                of past_modifiers, future_modifiers, 'at', or 'on'.
            start (str): The expression defining the date to apply the calculation to
            value (str): A string of digits
            unit (str): A string referencing time units defined by this module (eg. day, years, etc)

        Returns:
            datetime: The datetime object

        Raises:
            ParseError: If a date cannot be calculated from input
        """

        start = start.strip()
        if not start:
            start = self.now

        offset = self._parse_value(value, unit)
        start = self._parse_start(start)

        if modifier.lower() in ('at', 'on'):
            return start.as_seconds
        elif modifier.lower() in self.past_modifiers:
            return int(start) - offset
        elif modifier.lower() in self.future_modifiers:
            return int(start) + offset
        else:
            raise ParseError("Could not parse range modifier '{}'".format(modifier))

    def get_unit_class(self, unit):
        """
        Returns the class referenced by the unit string (Era, Year, Season, Span, Day, Hour, etc).
        Plurals will be stripped and capialization will be forced, so 'minutes' is equivalent to
        'Minute'.

        Args:
            unit (str): The name of the unit of time to look up in this module

        Returns:
            DateObject: The subclass of DateObject
        """
        names = [unit.title(), unit.title().rstrip('s')]
        for (name, obj) in inspect.getmembers(sys.modules[__name__], inspect.isclass):
            if name in names:
                return obj
        raise ParseError("Could not find a datetime object for {}".format(unit))


# helpful shortcuts for importing and hints for the parser
now = datetime(year=3206, season=8, day=12, era=3)
today = now
yesterday = today - Day.length_in_seconds
