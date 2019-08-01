"""
Module to get the current time in given time zones and in UTC.
"""
from datetime import datetime
from pytz import timezone

class ComTime:
    """
    Manages timezones and returns their time.
    """

    def __init__(self, time_zones=[]):
        self.time_zones = set(time_zones)
        self.time_zones.add("UTC")
        self.time_format = "%H:%M:%S - %d.%m.%Y"

    def time_message(self):
        """
        Builds a time message for the telegram bot.
        """
        time_string = ""
        time_strings = self._get_times()
        for zone in time_strings:
            time_string += "*{zone}*: {time}\n".format(zone=zone,
                                                       time=time_strings[zone])
        return time_string

    def _get_times(self):
        time_strings = {}
        for time_zone in self.time_zones:
            time = datetime.now(timezone(time_zone))
            time_strings[time_zone] = time.strftime(self.time_format)
        return time_strings
