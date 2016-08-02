# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import logging
import os
import sys
import importlib
import time
from datetime import datetime
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # add modules folder to path


class SubtitlesPlease(PatternMatchingEventHandler):
    def __init__(self, config_fp=None, patterns=None, ignore_patterns=None,
                 ignore_directories=False, case_sensitive=False):
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
            super(SubtitlesPlease, self).__init__(self.files, None, False, False)

            try:
                for mods in configs["subtitles-modules"]:
                    module_name, class_name = mods.split(":")
                    mod = importlib.import_module(name="modules.%s" % module_name)
                    cls = getattr(mod, class_name)
                    instance = cls()
                    self.modules.append(instance)
                    logging.info("Module %s loaded" % str(mods))
            except ImportError as ex:
                logging.error("Module import failed: %s" % ex)
        except Exception as ex:
            logging.error("Error loading configuration: %s" % ex)

    @staticmethod
    def get_file_and_location_from_path(source_file=""):
        file_list = source_file.split(os.sep)
        file_name = file_list[-1]
        file_location = source_file.split(file_name, 1)[0]
        return file_name, file_location

    def on_created(self, event):
        """
        This gets called when a video file is detected in the watched directories
        :param self:
        :param event:
        :return:
        """
        source_file = event.src_path
        file_name, location = self.get_file_and_location_from_path(source_file)
        logging.info("OnCreated Got Called: %s | %s" % (file_name, location))
        for module in self.modules:
            if module.get_subtitles(title=file_name, location=location):
                logging.info("Module %s found a suitable subtitle", str(module))
                break

    def run(self):
        """
        This sets up the watcher on the directories listed
        :return:
        """
        observers = []
        for directory in self.directories:
            observer = Observer()
            observer.schedule(self, directory, recursive=True)
            observer.start()
            observers.append(observer)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for observer in observers:
                observer.stop()
        for observer in observers:
            observer.join()


if __name__ == "__main__":
    import os as ops

    date_string = datetime.strftime(datetime.today(), "%Y%m%d")
    # put in log directory
    log_directory = ops.path.abspath(
        ops.path.join(__file__, "../..")) + ops.sep + "logs" + ops.sep + "error_%s.log" % date_string
    logging.basicConfig(filename=log_directory, level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s]:%(message)s')
    try:
        sub = SubtitlesPlease()
        sub.run()
    except Exception as ex:
        logging.error("Some shit occurred: %s", ex)
