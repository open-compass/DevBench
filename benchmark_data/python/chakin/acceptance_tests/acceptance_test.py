import os
import sys
import unittest
from unittest.mock import patch
import pandas as pd

from chakin.downloader import download, search

class TestDownloader(unittest.TestCase):

    @patch('chakin.downloader.urlretrieve')
    def test_download_acceptance(self, mock_urlretrieve):
        test_save_dir = os.path.join('chakin', 'test_downloads') 
        test_file_name = 'test.vec'
        test_save_path = os.path.join(test_save_dir, test_file_name)

        if not os.path.exists(test_save_dir):
            os.makedirs(test_save_dir)

        def fake_urlretrieve(url, filename, reporthook):
            with open(filename, 'wb') as f:
                f.write(os.urandom(1024))
            reporthook(1, 1024, 1024 * 1024)
            return filename, None

        mock_urlretrieve.side_effect = fake_urlretrieve

        download_result = download(number=0, save_dir=test_save_dir)
        self.assertTrue(os.path.isfile(download_result))

        if os.path.isfile(download_result):
            os.remove(download_result)
        if os.path.isdir(test_save_dir):
            os.rmdir(test_save_dir)

if __name__ == '__main__':
    unittest.main()
