#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_subtitlesplease
----------------------------------

Tests for `subtitles please` module.
"""

import sys
import unittest
from io import StringIO
from subtitlesplease import subtitlesplease


class TestSubtitlesPlease(unittest.TestCase):
    def setUp(self):
        config_file = StringIO(
            u"""
            {
                "watch-directories":["/Users/smurf/Downloads"],
                "file-types":["*.avi", "*.mp4", "*.mkv"],
                "subtitles-modules":["Subscene"]
            }
            """)
        self.subs = subtitlesplease.SubtitlesPlease(config_fp=config_file)

    def tearDown(self):
        pass

    def test_config_setup(self):
        self.assertEqual(["/Users/smurf/Downloads"], self.subs.directories)
        self.assertEqual(["*.avi", "*.mp4", "*.mkv"], self.subs.files)

    def test_default_config_setup(self):
        self.subs = subtitlesplease.SubtitlesPlease()
        self.assertEqual(["/Users/smurf/Downloads"], self.subs.directories)
        self.assertEqual(["*.avi", "*.mp4", "*.mkv"], self.subs.files)


if __name__ == '__main__':
    sys.exit(unittest.main())
