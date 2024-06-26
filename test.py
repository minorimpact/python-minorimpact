#!/usr/bin/env python3

import minorimpact
import os
import tempfile
import unittest
from unittest import mock
import random
import subprocess
import sys
import time

class TestUtils(unittest.TestCase):
    test_dir = None

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_001_md5dir(self):
        # create a new note based on position and title
        test_file = open('./foo', 'w')
        test_file.write('TEST')
        test_file.close()
        md5 = minorimpact.md5dir('./foo')
        self.assertEqual(md5, '8fae6cc0323499563d770dd63431dfb5')
        os.mkdir('subdir')
        test_file = open('./subdir/foo2', 'w')
        test_file.write('TEST2')
        test_file.close()
        md5 = minorimpact.md5dir('.')
        self.assertEqual(md5, '68bbcac5f5b058703d30e20989e2a484')
        size = minorimpact.dirsize('.')
        self.assertEqual(size, 9)

    def test_002_getChar(self):
        fd = sys.stdin.fileno()
        sys.stdin = mock.Mock()
        sys.stdin.read.return_value = '\n'
        sys.stdin.fileno.return_value = fd
        c = minorimpact.getChar(default='y').lower()
        self.assertEqual(c, 'y')
        c = minorimpact.getChar().lower()
        self.assertNotEqual(c, 'y')

    def test_003_randintodd(self):
        random.seed(1)
        rand = minorimpact.randintodd(1,1000)
        self.assertEqual(rand, 139)

    def test_004_duplicates(self):
        duplicate = minorimpact.checkforduplicates(pidfile='./pidfile')
        self.assertFalse(duplicate)
        duplicate = minorimpact.checkforduplicates(pidfile='./pidfile')
        self.assertTrue(duplicate)
        proc = subprocess.Popen(['python3', '-c', 'import time;time.sleep(5)']) 
        self.assertIsNone(proc.poll())
        with open('./pidfile', 'w') as p:
            p.write(str(proc.pid))
        minorimpact.killduplicates(pidfile='./pidfile')
        time.sleep(1)
        self.assertEqual(proc.poll(), -9)

    def test_005_readdir(self):
        os.mkdir('dir')
        with open('dir/one', 'a') as f:
            f.write('foo')
        os.mkdir('dir/dir')
        with open('dir/dir/two', 'a') as f:
            f.write('foo')
        files = minorimpact.readdir('dir')
        self.assertEqual(len(files), 2)

    def test_006_args(self):
        self.assertFalse(minorimpact.default_arg_flags.debug)
        self.assertFalse(minorimpact.default_arg_flags.yes)

    def test_007_cache(self):
        cache_file = './test.cache'
        cache = { 'test':2 }
        minorimpact.write_cache(cache_file, cache)

        cache = minorimpact.read_cache(cache_file)
        self.assertEqual(cache['test'], 2)

if __name__ == '__main__':
    unittest.main()

