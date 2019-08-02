"""
Module to interact with xkcd.com
"""
import random
from string import Template
import requests


class ComXkcd:
    """
    Class to query xkcd for the newest, a specific or a random xkcd comic.
    """
    WRONG_USAGE = "Please call /xkcd either without an argument or " + \
                  "supply a single positive number or the keyword 'random' " + \
                  "as an argument."

    def __init__(self):
        self.request_template = Template("http://xkcd.com/$num/info.0.json")
        self.xkcd_newest_json = "http://xkcd.com/info.0.json"


    def get_xkcd(self, argument):
        """
        Parses which xkcd to return.
        """
        if not argument:
            return self._get_newest_xkcd()
        if argument[0].isdigit() and int(argument[0]) >= 0:
            return self._get_xkcd_number(int(argument[0]))
        if argument[0] == "random":
            return self._get_random_xkcd()
        return (None, None)

    def _get_newest_xkcd(self):
        newest_xkcd_entry = self._get_newest_xkcd_entry()
        return (newest_xkcd_entry['img'], newest_xkcd_entry['alt'])

    def _get_xkcd_number(self, xkcd_number):
        specified_xkcd_query = self.request_template.substitute(num=xkcd_number)
        specified_xkcd_entry = requests.get(specified_xkcd_query).json()
        return (specified_xkcd_entry['img'], specified_xkcd_entry['alt'])

    def _get_random_xkcd(self):
        random_xkcd_number = random.randrange(1,
                                              self._get_highest_xkcd_number())
        random_xkcd_query = self.request_template.substitute(num=random_xkcd_number)
        random_xkcd_entry = requests.get(random_xkcd_query).json()
        return (random_xkcd_entry['img'], random_xkcd_entry['alt'])

    def _get_highest_xkcd_number(self):
        """
        Determines the highest xkcd comic's number by checking the latest comic.
        """
        return self._get_newest_xkcd_entry()['num']

    def _get_newest_xkcd_entry(self):
        return requests.get(self.xkcd_newest_json).json()
