import logging
import requests
from bs4 import BeautifulSoup
from modules.basesubtitles import BaseSubtitles


class Subscene(BaseSubtitles):
    """
    This module is responsible for getting subtiles from subscene.com
    """
    SEARCH_URL = "https://subscene.com/subtitles/release?q="

    def get_subtitles(self, title=None, location=None):
        """
        Get the subtitles in 3 phases
        1) query for title
        2) select the best subtitle
        3) download the subtitle to location
        :param title: Video title to search for
        :param location: location on the filesystem to store subtitle
        :return: True of subtitle was found false otherwise
        """
        logging.info("%s Getting title of %s to store %s" % (str(self), title, location))
        subtitle_list = self.query_subscene(title=title)

    def __str__(self):
        return "Subscene"

    def query_subscene(self, title):
        r = requests.post(url=self.SEARCH_URL + title)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, "html.parser")
        return html_doc


class SubsceneSubs(object):

    def __init__(self, language="English", title="", owner=""):
        self.language = language
        self.title = title
        self.owner = owner
