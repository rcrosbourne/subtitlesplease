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
from subtitlesplease.subtitlesplease import SubtitlesPlease
from modules.subscene import Subscene


class TestSubtitlesPlease(unittest.TestCase):
    def setUp(self):
        config_file = StringIO(
            u"""
            {
                "watch-directories":["/Users/smurf/Downloads"],
                "file-types":["*.avi", "*.mp4", "*.mkv"],
                "subtitles-modules":["subscene:Subscene", "opensubtitles:OpenSubtitles"]
            }
            """)
        self.subs = SubtitlesPlease(config_fp=config_file)
        self.subscene = Subscene()

    def tearDown(self):
        pass

    def test_config_setup(self):
        self.assertEqual(["/Users/smurf/Downloads"], self.subs.directories)
        self.assertEqual(["*.avi", "*.mp4", "*.mkv"], self.subs.files)

    def test_default_config_setup(self):
        self.subs = SubtitlesPlease()
        self.assertEqual(["/Users/smurf/Downloads"], self.subs.directories)
        self.assertEqual(["*.avi", "*.mp4", "*.mkv"], self.subs.files)

    def test_subscene_module_loaded(self):
        subscene = self.subs.modules[0]
        self.assertEqual("Subscene", str(subscene))

    def test_opensubtitles_module_loaded(self):
        openSubs = self.subs.modules[1]
        self.assertEqual("OpenSubtitles", str(openSubs))

    def test_subscene_query_subscene(self):
        docs = self.subscene.get_subtitles(title="Menace.II.Society.1993.1080p.BluRay.x264.YIFY.mp4",
                                           location="/Users/smurf/Downloads")
        self.assertIsNotNone(docs)


if __name__ == '__main__':
    sys.exit(unittest.main())
