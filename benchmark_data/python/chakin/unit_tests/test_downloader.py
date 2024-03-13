import os
import unittest
from unittest.mock import patch, MagicMock

from chakin.downloader import load_datasets, download

class TestDownloader(unittest.TestCase):

    name = 'word2vec.Wiki-NEologd.50d'
    number = 22

    @patch('chakin.downloader.urlretrieve')
    def test_download_by_name(self, mock_urlretrieve):
        test_save_dir = './test_download'
        test_file_name = self.name + '.vec'
        test_save_path = os.path.join(test_save_dir, test_file_name)

        if not os.path.exists(test_save_dir):
            os.makedirs(test_save_dir)

        def fake_urlretrieve(url, filename, reporthook):
            with open(filename, 'wb') as f:
                f.write(os.urandom(1024))
            reporthook(1, 1024, 1024 * 1024)
            return filename, MagicMock()

        mock_urlretrieve.side_effect = fake_urlretrieve

        download_result = download(name=self.name, save_dir=test_save_dir)
        self.assertTrue(os.path.isfile(download_result))
        self.assertEqual(os.path.getsize(download_result), 1024)

        os.remove(download_result)
        os.rmdir(test_save_dir)


if __name__ == '__main__':
    unittest.main()
