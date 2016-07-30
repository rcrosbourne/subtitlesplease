#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_subtitlesplease
----------------------------------

Tests for `subtitlesplease` module.
"""

import sys
import unittest
from subtitlesplease import subtitlesplease


class TestSubtitlesPlease(unittest.TestCase):
    def setUp(self):
        self.subs = subtitlesplease.SubtitlesPlease()

    def tearDown(self):
        pass

    def test_config_setup(self):
        self.assertEqual(["/Users/smurf/Downloads"], self.subs.directories)
        self.assertEqual(["*.avi", "*.mp4", "*.mkv"], self.subs.files)


if __name__ == '__main__':
    sys.exit(unittest.main())
