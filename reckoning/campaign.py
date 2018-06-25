"""
The Campaign clock for the Noobhammer Chronicles
"""
from telisaran import datetime
from calendar import Calendar
import os
import yaml
import fire


class Timeline:
    """
    Manage the events of a campaign timeline.
    """

    def __init__(self, datafile=None):
        self._datafile = datafile
        self._yaml_config()
        self._load()

    def _load(self):
        """
        Load events from a YAML file.
        """
        self._events = dict()
        if self._datafile:
            with open(self._datafile, 'r') as f:
                self._events = yaml.load(f)

    def _write(self):
        """
        Write timeline events to a YAML file.
        """
        if self._datafile:
            with open(self._datafile, 'w') as f:
                f.write(self.as_yaml)

    def _yaml_config(self):
        """
        Configure the PyYAML library to represent datetime objects as integer seconds
        """
        def yaml_representer(dumper, data):
            return dumper.represent_scalar(u'telisaran.datetime', str(int(data)))

        def yaml_constructor(loader, node):
            return datetime.from_seconds(int(loader.construct_scalar(node)))

        yaml.add_representer(datetime, yaml_representer)
        yaml.add_constructor(u'telisaran.datetime', yaml_constructor)

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
        return self.list

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
        self._add(description, datetime.from_expression(expression, timeline=self._events))
        self._write()
        return self.list

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
    def as_yaml(self):
        """as-yaml

        Description:
            Dump the timeline of events as YAML
        """
        return yaml.dump(self._events)

    def __str__(self):
        return "The Noobhammer Chronicles Campaign Timeline"

    def __repr__(self):
        return str(self) + "\n".join(list(self.list))


class Campaign:
    """
    The timeline of major events in the campaign.
    """

    def __init__(self):
        datafile = os.path.join(os.path.expanduser('~'), '.campaign_timeline.yaml')
        self.calendar = Calendar()
        self.timeline = Timeline(datafile)


if '__main__' == __name__:
    fire.Fire(Campaign())
