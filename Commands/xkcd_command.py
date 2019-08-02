"""
Module to interact with xkcd.com
"""
import random
import requests
from string import Template


XKCD_REQUEST_TEMPLATE = Template("http://xkcd.com/$num/info.0.json")


def get_xkcd(argument):
    """
    Parses which xkcd to return.
    """
    if not argument:
        return _get_newest_xkcd()
    if argument[0].isdigit() and int(argument[0]) >= 0:
        return _get_xkcd_number(int(argument[0]))
    if argument[0] == "random":
        return _get_random_xkcd()
    return None


def _get_newest_xkcd():
    newest_xkcd_entry = _get_newest_xkcd_entry()
    return (newest_xkcd_entry['img'], newest_xkcd_entry['alt'])


def _get_xkcd_number(xkcd_number):
    global XKCD_REQUEST_TEMPLATE
    specified_xkcd_query = XKCD_REQUEST_TEMPLATE.substitute(num=xkcd_number)
    specified_xkcd_entry = requests.get(specified_xkcd_query).json()
    return (specified_xkcd_entry['img'], specified_xkcd_entry['alt'])

def _get_random_xkcd():
    global XKCD_REQUEST_TEMPLATE
    random_xkcd_number = random.randrange(1, _get_highest_xkcd_number())
    random_xkcd_query = XKCD_REQUEST_TEMPLATE.substitute(num=random_xkcd_number)
    random_xkcd_entry = requests.get(random_xkcd_query).json()
    return (random_xkcd_entry['img'], random_xkcd_entry['alt'])

def _get_highest_xkcd_number():
    """
    Determines the highest xkcd comic's number by checking the latest comic.
    """
    return _get_newest_xkcd_entry()['num']

def _get_newest_xkcd_entry():
    xkcd_newest_json = "http://xkcd.com/info.0.json"
    return requests.get(xkcd_newest_json).json()
