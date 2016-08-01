from modules.basesubtitles import BaseSubtitles
import logging


class Subscene(BaseSubtitles):
    """
    This module is responsible for getting subtiles from subscene.com
    """

    def get_subtitles(self, title=None, location=None):
        logging.info("%s Getting title of %s to store %s" % (str(self), title, location))

    def __str__(self):
        return "Subscene"
