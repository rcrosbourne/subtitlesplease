# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import logging
import os
import importlib


class SubtitlesPlease(object):

    def __init__(self, config_fp=None):
        """
        This initailized the Subtitle object.
        :param config_fp: This is a file pointer or anything that response to fp.read()
        """
        try:
            self.directories = []
            self.files = []
            self.modules = []
            if config_fp:
                configs = json.load(config_fp)
            else:
                config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + "config.json"
                fp = open(config_file, "r")
                configs = json.load(fp)
                fp.close()
            self.directories = configs["watch-directories"]
            self.files = configs["file-types"]
            try:
                for mods in configs["subtitles-modules"]:
                    module_name, class_name = mods.split(":")
                    mod = importlib.import_module(name="modules.%s" % module_name)
                    cls = getattr(mod, class_name)
                    instance = cls()
                    self.modules.append(instance)
            except ImportError as ex:
                logging.error("Module import failed: %s" % ex)
        except Exception as ex:
            logging.error("Error loading configuration: %s" % ex)

    def run(self):
        """
        This sets up the watcher on the directories listed

        :return:
        """
