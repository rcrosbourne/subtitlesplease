from abc import ABCMeta, abstractmethod


class BaseSubtitles(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_subtitles(self, title=None, location=None, language=None):
        """This function gets uses the file name and gets returns the subtitle file in file_location"""
        pass
