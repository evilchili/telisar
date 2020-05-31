"""
The Campaign clock for the Noobhammer Chronicles
"""
from telisar.reckoning import telisaran
import json


class Timeline:
    """
    Manage the events of a campaign timeline.
    """

    def __init__(self, datafile=None):
        self._datafile = datafile
        self._load()

    def _load(self):
        """
        Load events from a JSON file.
        """
        self._events = dict()
        if self._datafile:
            with open(self._datafile, 'r') as f:
                self._events = json.load(f)
            for (event, timestamp) in self._events.items():
                self._events[event] = telisaran.datetime.from_seconds(timestamp)

    def _write(self):
        """
        Write timeline events to a JSON file.
        """
        if self._datafile:
            with open(self._datafile, 'w') as f:
                f.write(self.as_json)

    def _add(self, description, date):
        """
        Add an event to the timeline.

        Args:
            description (str): The text of the event
            date (datetime): The datetime associated with the event
        """
        self._events[description.title()] = date
        return self._events.get(description)

    def _del(self, description):
        """
        Remove the specified event from the timeline.

        Args:
            description (str): The text of the event
        """
        del self._events[description.title()]

    # CLI entry-points

    def expunge(self, description):
        """expunge

        Description:
            Expunge all record of an historical event.

        Examples:

            expunge "TPK on 2.4839.7.23"

        Parameters:

        DESCRIPTION   The description of the event
        """
        self._del(description)
        self._write()
        return repr(self)

    def record(self, description, expression):
        """record

        Description:
            Add a new event to the historical record.

        Examples:

            record "Start of the campaign" "on 2.4839.7.22"
            record "BBEG starts reign of destruction" "50 years before start of the campaign"
            record "TPK on tomorrow"

        Parameters:

        DESCRIPTION   The description of the event
        EXPRESSION    When the event occurred.

        """
        self._add(description, telisaran.datetime.from_expression(expression, timeline=self._events))
        self._write()
        return repr(self)

    @property
    def list(self):
        """list

        Description:
            List the events of the timeline.
        """
        for description in sorted(self._events, key=self._events.get):
            yield("{} {}  {}".format(
                self._events.get(description).numeric_date,
                self._events.get(description).date,
                description
            ))

    @property
    def as_json(self):

        def serializer(obj):
            if isinstance(obj, telisaran.datetime):
                return int(obj)
        return json.dumps(self._events, default=serializer)

    @property
    def as_markdown(self):
        """as-markdown

        Description:
            Dump the timeline of events as a markdown-formatted list.
        """
        yield "#### {}".format(str(self))
        for description in sorted(self._events, key=self._events.get):
            yield("* *{} {}*  {}".format(
                self._events.get(description).numeric_date,
                self._events.get(description).date,
                description
            ))

    def __str__(self):
        return "The Noobhammer Chronicles Campaign Timeline\n" + "\n".join(list(self.list))
