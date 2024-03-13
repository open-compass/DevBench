import unittest
import readtime
from readtime.api import of_text

class BaseTestCase(unittest.TestCase):
    def test_plain_text_empty(self):
        """
        Test case for calculating read time of empty plain text.
        """
        result = of_text('')
        self.assertEqual(result.seconds, 1)
        self.assertEqual(result.text, '1 min')
        self.assertEqual(str(result), '1 min read')

    def test_plain_text_null(self):
        """
        Test case for calculating read time of null plain text.
        """
        result = of_text(None)
        self.assertEqual(result.seconds, 0)
        self.assertEqual(result.text, '1 min')
        self.assertEqual(str(result), '1 min read')

    def test_unsupported_format(self):
        """
        Test case for unsupported format.
        """
        with self.assertRaises(Exception) as e:
            readtime.utils.read_time('Some simple text', format='foo')
        self.assertEqual(str(e.exception), 'Unsupported format: foo')

    def test_invalid_format(self):
        """
        Test case for invalid format.
        """
        with self.assertRaises(Exception) as e:
            readtime.utils.read_time('Some simple text', format=123)
        self.assertEqual(str(e.exception), 'Unsupported format: 123')


