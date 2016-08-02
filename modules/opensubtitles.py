from modules.basesubtitles import BaseSubtitles
import logging


class OpenSubtitles(BaseSubtitles):

    def get_subtitles(self, title=None, location=None, language=None):
        logging.info("%s Getting title of %s to store %s" % (str(self), title, location))

    def __str__(self):
        return "OpenSubtitles"
