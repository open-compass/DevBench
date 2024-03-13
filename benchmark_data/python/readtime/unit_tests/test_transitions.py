import unittest
from readtime.api import of_text


class BaseTestCase(unittest.TestCase):
    def test_transitions(self):
        """
        Test the transitions between different read time durations.
        """
        word = 'word '
        for x in range(10):

            # test the maximum num words for x read time
            text = word * 265 * x
            result = of_text(text)
            self.assertEqual(result.seconds, x * 60 if x > 0 else 1)
            self.assertEqual(result.text, f'{x if x > 0 else 1} min')
            self.assertEqual(str(result), f'{x if x > 0 else 1} min read')

            # test the maximum + 1 num words, and make sure read time is x + 1
            text += 'word'
            result = of_text(text)
            self.assertEqual(result.seconds, x * 60 + 1)
            self.assertEqual(result.text, f'{x + 1} min')
            self.assertEqual(str(result), f'{x + 1} min read')
