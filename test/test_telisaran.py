import pytest
from telisar.reckoning import telisaran
import random

ONE_DAY_IN_SECONDS = 86400
ONE_SEASON_IN_SECONDS = ONE_DAY_IN_SECONDS * 45
ONE_YEAR_IN_SECONDS = ONE_DAY_IN_SECONDS * 365
FIRST_ERA = 20000 * ONE_YEAR_IN_SECONDS
SECOND_ERA = 10000 * ONE_YEAR_IN_SECONDS


def random_datetime():
    """
    Generate random datetimes from the standard calendar
    """
    era = random.choice(range(len(telisaran.Era.years)))
    max_year = 20000 if era == 2 else telisaran.Era.years[era]
    return telisaran.datetime(
        era=era + 1,
        year=random.choice(range(1, max_year + 1)),
        season=random.choice(range(1, telisaran.Year.length_in_seasons + 1)),
        day=random.choice(range(1, telisaran.Season.length_in_days + 1)),
        hour=random.choice(range(24)),
        minute=random.choice(range(60)),
        second=random.choice(range(60))
    )


def random_festival_datetime():
    """
    Generate random datetimes that fall in the festival of the hunt
    """
    era = random.choice(range(len(telisaran.Era.years)))
    max_year = 20000 if era == 2 else telisaran.Era.years[era]
    return telisaran.datetime(
        era=era + 1,
        year=random.choice(range(1, max_year + 1)),
        season=9,
        day=random.choice(range(1, telisaran.FestivalOfTheHunt.length_in_days + 1)),
        hour=random.choice(range(24)),
        minute=random.choice(range(60)),
        second=random.choice(range(60))
    )


# generate test fixtures
fixtures = [random_datetime() for i in range(1000)]
festival_fixtures = [random_festival_datetime() for i in range(100)]


@pytest.mark.parametrize('dt', fixtures, ids=[f.short for f in fixtures])
def test_datetime_standard(dt):
    """
    Test internal consistency of randomized datetime objects
    """
    assert int(dt) == telisaran.datetime.from_seconds(int(dt))
    assert dt.long
    assert dt.short
    assert dt.numeric
    assert dt.date
    assert dt.time
    assert dt.time_short
    assert repr(dt)
    assert str(dt)


@pytest.mark.parametrize('dt', festival_fixtures, ids=[f.short for f in festival_fixtures])
def test_datetime_festival(dt):
    """
    Test internal consistency of randomized datetime objects on the festival of the hunt
    """
    assert int(dt) == telisaran.datetime.from_seconds(int(dt))
    assert dt.long
    assert dt.short
    assert dt.numeric
    assert dt.date
    assert dt.time
    assert dt.time_short
    assert repr(dt)
    assert str(dt)


@pytest.mark.parametrize('kwargs, expected', [
    (dict(era=1, year=1, season=1, day=1), 0),
    (dict(era=1, year=1, season=1, day=2), ONE_DAY_IN_SECONDS),
    (dict(era=1, year=1, season=1, day=3), ONE_DAY_IN_SECONDS * 2),
    (dict(era=1, year=1, season=1, day=45), ONE_DAY_IN_SECONDS * 44),
    (dict(era=1, year=1, season=2, day=1), ONE_SEASON_IN_SECONDS),
    (dict(era=1, year=1, season=2, day=2), ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS),
    (dict(era=1, year=1, season=2, day=3), ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS * 2),
    (dict(era=1, year=1, season=2, day=45), ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS * 44),
    (dict(era=1, year=1, season=8, day=1), ONE_SEASON_IN_SECONDS * 7),
    (dict(era=1, year=1, season=8, day=2), ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS),
    (dict(era=1, year=1, season=8, day=3), ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS * 2),
    (dict(era=1, year=1, season=8, day=45), ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS * 44),
    (dict(era=1, year=1, season=9, day=1), ONE_SEASON_IN_SECONDS * 8),
    (dict(era=1, year=1, season=9, day=5), ONE_SEASON_IN_SECONDS * 8 + ONE_DAY_IN_SECONDS * 4),

    (dict(era=1, year=2, season=1, day=1), ONE_YEAR_IN_SECONDS),
    (dict(era=1, year=2, season=1, day=2), ONE_YEAR_IN_SECONDS + ONE_DAY_IN_SECONDS),
    (dict(era=1, year=2, season=1, day=3), ONE_YEAR_IN_SECONDS + ONE_DAY_IN_SECONDS * 2),
    (dict(era=1, year=2, season=1, day=45), ONE_YEAR_IN_SECONDS + ONE_DAY_IN_SECONDS * 44),
    (dict(era=1, year=2, season=2, day=1), ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS),
    (dict(era=1, year=2, season=2, day=2), ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS),
    (dict(era=1, year=2, season=2, day=3), ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS * 2),
    (dict(era=1, year=2, season=2, day=45), ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS * 44),
    (dict(era=1, year=2, season=8, day=1), ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7),
    (dict(era=1, year=2, season=8, day=2), ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS),
    (dict(era=1, year=2, season=8, day=3), ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS * 2),
    (dict(era=1, year=2, season=8, day=45), ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS * 44),
    (dict(era=1, year=2, season=9, day=1), ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 8),
    (dict(era=1, year=2, season=9, day=5), ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 8 + ONE_DAY_IN_SECONDS * 4),

    (dict(era=2, year=2, season=1, day=1), FIRST_ERA + ONE_YEAR_IN_SECONDS),
    (dict(era=2, year=2, season=1, day=2), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_DAY_IN_SECONDS),
    (dict(era=2, year=2, season=1, day=3), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_DAY_IN_SECONDS * 2),
    (dict(era=2, year=2, season=1, day=45), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_DAY_IN_SECONDS * 44),
    (dict(era=2, year=2, season=2, day=1), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS),
    (dict(era=2, year=2, season=2, day=2), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS),
    (dict(era=2, year=2, season=2, day=3), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS * 2),
    (dict(era=2, year=2, season=2, day=45), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS * 44),
    (dict(era=2, year=2, season=8, day=1), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7),
    (dict(era=2, year=2, season=8, day=2), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS),
    (dict(era=2, year=2, season=8, day=3), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS * 2),
    (dict(era=2, year=2, season=8, day=45), FIRST_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS * 44),
    (dict(era=2, year=1, season=9, day=1), FIRST_ERA + ONE_SEASON_IN_SECONDS * 8),
    (dict(era=2, year=1, season=9, day=5), FIRST_ERA + ONE_SEASON_IN_SECONDS * 8 + ONE_DAY_IN_SECONDS * 4),

    (dict(era=3, year=2, season=1, day=1), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS),
    (dict(era=3, year=2, season=1, day=2), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_DAY_IN_SECONDS),
    (dict(era=3, year=2, season=1, day=3), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_DAY_IN_SECONDS * 2),
    (dict(era=3, year=2, season=1, day=45), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_DAY_IN_SECONDS * 44),
    (dict(era=3, year=2, season=2, day=1), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS),
    (dict(era=3, year=2, season=2, day=2), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS),
    (dict(era=3, year=2, season=2, day=3), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS * 2),
    (dict(era=3, year=2, season=2, day=45), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS + ONE_DAY_IN_SECONDS * 44),
    (dict(era=3, year=2, season=8, day=1), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7),
    (dict(era=3, year=2, season=8, day=2), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS),
    (dict(era=3, year=2, season=8, day=3), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS * 2),
    (dict(era=3, year=2, season=8, day=45), FIRST_ERA + SECOND_ERA + ONE_YEAR_IN_SECONDS + ONE_SEASON_IN_SECONDS * 7 + ONE_DAY_IN_SECONDS * 44),
    (dict(era=3, year=1, season=9, day=1), FIRST_ERA + SECOND_ERA + ONE_SEASON_IN_SECONDS * 8),
    (dict(era=3, year=1, season=9, day=5), FIRST_ERA + SECOND_ERA + ONE_SEASON_IN_SECONDS * 8 + ONE_DAY_IN_SECONDS * 4),

    (dict(era=1, year=1, season=1, day=1, hour=1), 3600),
    (dict(era=1, year=1, season=1, day=1, hour=1, minute=1), 3660),
    (dict(era=1, year=1, season=1, day=1, hour=1, minute=3, second=57), 3837),
])
def test_datetime_arithmetic(kwargs, expected):
    """
    Test the edge cases of datetime arithmetic
    """
    dt = telisaran.datetime(**kwargs)
    edt = telisaran.datetime.from_seconds(expected)
    assert dt == edt
    assert int(dt) == expected


@pytest.mark.parametrize('kwargs, expected', [
    # bad eras
    (dict(era=0, year=1, season=1, day=1), telisaran.InvalidEraError),
    (dict(era=-1, year=1, season=1, day=1), telisaran.InvalidEraError),
    (dict(era=4, year=1, season=1, day=1), telisaran.InvalidEraError),

    # bad years
    (dict(era=1, year=0, season=1, day=1), telisaran.InvalidYearError),
    (dict(era=1, year=-1, season=1, day=1), telisaran.InvalidYearError),
    (dict(era=1, year=20001, season=1, day=1), telisaran.InvalidYearError),
    (dict(era=2, year=10001, season=1, day=1), telisaran.InvalidYearError),

    # bad seasons
    (dict(era=1, year=1, season=0, day=1), telisaran.InvalidSeasonError),
    (dict(era=1, year=1, season=-1, day=1), telisaran.InvalidSeasonError),
    (dict(era=1, year=1, season=10, day=1), telisaran.InvalidSeasonError),

    # bad days
    (dict(era=1, year=1, season=1, day=0), telisaran.InvalidDayError),
    (dict(era=1, year=1, season=1, day=-1), telisaran.InvalidDayError),
    (dict(era=1, year=1, season=1, day=46), telisaran.InvalidDayError),

    # bad hour
    (dict(era=1, year=1, season=1, day=1, hour=-1), telisaran.InvalidHourError),
    (dict(era=1, year=1, season=1, day=1, hour=24), telisaran.InvalidHourError),
    (dict(era=1, year=1, season=1, day=1, hour=1, minute=-1), telisaran.InvalidMinuteError),
    (dict(era=1, year=1, season=1, day=1, hour=1, minute=60), telisaran.InvalidMinuteError),
    (dict(era=1, year=1, season=1, day=1, hour=1, minute=1, second=-1), telisaran.InvalidSecondError),
    (dict(era=1, year=1, season=1, day=1, hour=1, minute=1, second=60), telisaran.InvalidSecondError),

])
def test_datetime_invalid(kwargs, expected):
    with pytest.raises(expected):
        telisaran.datetime(**kwargs)


def test_datetime_comparisons():
    black_hour = telisaran.datetime(era=1, year=3206, season=9, day=2)
    souls_hour = telisaran.datetime(era=1, year=3206, season=9, day=2, hour=6)
    assert black_hour < souls_hour
    assert black_hour <= souls_hour
    assert souls_hour > black_hour
    assert souls_hour >= black_hour


@pytest.mark.parametrize('expression, expected', [
    ('1 day ago', {'value': '1', 'unit': 'day', 'modifier': 'ago'}),
])
def test_parser_pattern(expression, expected):
    for pattern in telisaran.parser.patterns:
        m = pattern.match(expression)
        if not m:
            continue
        print(f"{m.groupdict()} == {expected}")
        assert m.groupdict() == expected
        return True
    pytest.fail(f"Expression was not matched by any pattern!")
