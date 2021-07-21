#!/usr/bin/env python3

import minorimpact
import os
import tempfile
import unittest

class TestNote(unittest.TestCase):

    test_dir = None

    #def __init__(self, methodName):
    #    super(TestNote, self).__init__(methodName)
    #    self.test_dir = os.getcwd()

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_001_md5dir(self):
        # create a new note based on position and title
        test_file = open("./foo", "w")
        test_file.write("TEST")
        test_file.close()
        md5 = minorimpact.md5dir("./foo")
        self.assertEqual(md5, "8fae6cc0323499563d770dd63431dfb5")
        os.mkdir("subdir")
        test_file = open("./subdir/foo2", "w")
        test_file.write("TEST2")
        test_file.close()
        md5 = minorimpact.md5dir(".")
        self.assertEqual(md5, "68bbcac5f5b058703d30e20989e2a484")
        size = minorimpact.dirsize(".")
        self.assertEqual(size, 9)


if __name__ == "__main__":
    unittest.main()
