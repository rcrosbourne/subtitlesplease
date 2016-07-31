# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import json
import logging


class SubtitlesPlease(object):

    def __init__(self, config_fp=None):
        """
        This initailized the Subtile object.
        :param config_fp: This is a file pointer or anything that response to fp.read()
        """
        try:
            self.directories = []
            self.files = []
            if config_fp:
                configs = json.load(config_fp)
            else:
                config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + "config.json"
                fp = open(config_file, "r")
                configs = json.load(fp)
                fp.close()
            self.directories = configs["watch-directories"]
            self.files = configs["file-types"]
        except Exception as ex:
            logging.error("Error loading configuration: %s" % ex)

    def run(self):
        """
        This runs indefinately
        :return:
        """
