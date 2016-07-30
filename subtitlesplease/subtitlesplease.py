# -*- coding: utf-8 -*-
import os
import json


class SubtitlesPlease(object):
    def __init__(self, config=None):
        if config:
            fp = open(config, "r")
            configs = json.load(fp)
            fp.close()
            self.directories = configs["watch-directories"]
            self.files = configs["file-types"]
        else:
            config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + "config.json"
            fp = open(config_file, "r")
            configs = json.load(fp)
            fp.close()
            self.directories = configs["watch-directories"]
            self.files = configs["file-types"]

