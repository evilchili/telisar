"""
The Campaign clock for the Noobhammer Chronicles
"""
from telisar.reckoning import telisaran
import collections
import json


event_properties = ['timestamp', 'redacted']
Event = collections.namedtuple('Event', event_properties)


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

            for (event, attrs) in self._events.items():
                attrs[0] = telisaran.datetime.from_seconds(attrs[0])
                self._events[event] = Event(**dict(zip(event_properties, attrs)))

    def _write(self):
        """
        Write timeline events to a JSON file.
        """
        if self._datafile:
            with open(self._datafile, 'w') as f:
                f.write(self.as_json)

    def _add(self, description, date, redacted=False):
        """
        Add an event to the timeline.

        Args:
            description (str): The text of the event
            date (datetime): The datetime associated with the event
            redacted (boolean): If True, do not include it in the public timeline
        """
        self._events[description.title()] = Event(timestamp=date, redacted=redacted)
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

    def record(self, description, expression, redacted=False):
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
        REDACTED      If True, do not include this event in the public timeline.

        """
        self._add(description, telisaran.datetime.from_expression(expression, timeline=self._events), redacted=redacted)
        self._write()
        return repr(self)

    @property
    def list(self):
        """list

        Description:
            List the events of the timeline.
        """
        markdown = ''.join(list(self.as_markdown)[1:])
        plaintext = markdown.replace('*', '').replace('#', '').replace('|', '')
        return plaintext

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
        yield("|= Date |= Event")
        for (description, event) in sorted(self._events.items(), key=lambda e: e[1].timestamp):
            if event.redacted:
                description = 'REDACTED'
            yield(f'| *{event.timestamp.numeric_date} {event.timestamp.date}* | {description}\n')

    def __str__(self):
        return self.list
