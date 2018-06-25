"""
A Telisaran calendaring tool.
"""
import telisaran
import fire


class Calendar:
    """.

    The Telisaran Calendar

    Syfdag kindle fate’s first light
    Mimdag have a secret might
    Wodag have the strength to fight
    Thordag curse the wrong, avenge the right
    Freydag love fair beauty’s sight

        – Dwarven nursery rhyme

    """

    def __init__(self, today=None, start=None, end=None):

        self.today = today
        if not self.today:
            self.today = telisaran.today

        self._end = end or self.today

        if start:
            self._start = start
        else:
            self._start = telisaran.datetime(
                year=self._end.year.year,
                season=self._end.season.season_of_year,
                day=1
            )

    def season(self):
        print(self._start.season.name.upper().center(14))
        print(" ".join([n[0:2] for n in telisaran.Day.names]))
        chunks = []
        for day in self._start.season.days:
            chunks.append("{:02d}".format(day.day_of_season))
            if day.day_of_span == telisaran.Span.length_in_days:
                print(" ".join(chunks))
                chunks = []

    @property
    def yesterday(self):
        try:
            return self.today - telisaran.Day.length_in_seconds
        except telisaran.InvalidDayError:
            return "Mortals cannot go back before the beginning of time."

    @property
    def tomorrow(self):
        return self.today + telisaran.Day.length_in_seconds

    def __repr__(self):
        return "The Telisaran Calendar"

if '__main__' == __name__:
    fire.Fire(Calendar())
