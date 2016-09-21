# -*- coding: utf-8 -*-

from .context import null

import unittest
import os
import random
import time
from multiprocessing import JoinableQueue


class ScanTestSuite(unittest.TestCase):
    """Basic test cases."""

    TEST_DIR = './test_directory'
    TEST_FILE_NAME = 'test.zip'

    def setUp(self):
        # Create a temporary file to scan
        os.mkdir(ScanTestSuite.TEST_DIR)
        self.name = os.path.normpath(os.path.join(
            ScanTestSuite.TEST_DIR, ScanTestSuite.TEST_FILE_NAME))
        writeNullFile(name=self.name, total_bytes=(
            4 * 1024 * 1024), null_bytes=(4 * 1024 * 1024 * .25))

        self.work = JoinableQueue()
        self.results = JoinableQueue()
        self.null_char = b'\x00'
        self.worker_list = null.create_workers(
            self.work, self.results, self.null_char)

    def tearDown(self):
        # Terminate worker processes and remove the temporary files
        for worker in self.worker_list:
            worker.terminate()

        os.remove(self.name)
        os.rmdir(ScanTestSuite.TEST_DIR)

    def test_Scan_count(self):
        count = null.scan(self.name, self.work, self.results)
        size = os.stat(self.name).st_size
        target_null_count = 4 * 1024 * 1024 * .25

        self.assertTrue(target_null_count - 1 <=
                        count <= target_null_count + 1)

    def test_Scan_count_false(self):
        count = null.scan(self.name, self.work, self.results)
        size = os.stat(self.name).st_size
        target_null_count = 1 * 1024 * 1024 * .25

        self.assertFalse(target_null_count - 1 <=
                        count <= target_null_count + 1)


def writeNullFile(name, total_bytes, null_bytes, null_char=b'\x00'):

    if null_bytes > total_bytes:
        raise ValueError(
            "total_bytes must be greater than or equal to null_bytes.")

    with open(name, 'wb') as file:
        file.seek(null_bytes)
        file.write(null_char)

        while file.tell() < total_bytes:
            file.write(chr(random.randint(1, 255)))


if __name__ == '__main__':
    unittest.main()