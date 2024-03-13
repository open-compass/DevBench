import unittest
from readtime.api import of_text, of_markdown, of_html


class BaseTestCase(unittest.TestCase):
    def test_plain_text(self):
        """
        Test case for calculating read time of plain text.
        """
        inp = open('samples/plain_text.txt').read()
        result = of_text(inp)
        self.assertEqual(result.seconds, 154)
        self.assertEqual(type(result.seconds), int)
        self.assertEqual(result.text, '3 min')
        self.assertEqual(str(result), '3 min read')

    def test_markdown(self):
        """
        Test case for calculating read time of markdown.
        """
        inp = open('samples/markdown.md').read()
        result = of_markdown(inp)
        self.assertEqual(result.seconds, 236)
        self.assertEqual(result.text, '4 min')
        self.assertEqual(str(result), '4 min read')

    def test_html(self):
        """
        Test case for calculating read time of html.
        """
        inp = open('samples/html.html').read()
        result = of_html(inp)
        self.assertEqual(result.seconds, 236)
        self.assertEqual(result.text, '4 min')
        self.assertEqual(str(result), '4 min read')

    def test_can_add(self):
        """
        Test case for adding two readtime objects.
        """
        inp = open('samples/plain_text.txt').read()
        result1 = of_text(inp)
        self.assertEqual(result1.seconds, 154)

        inp = open('samples/markdown.md').read()
        result2 = of_markdown(inp)
        self.assertEqual(result2.seconds, 236)

        result = (result1 + result2)
        self.assertEqual(result.seconds, 154 + 236)
        self.assertEqual(type(result.seconds), int)
        self.assertEqual(result.text, '7 min')
        self.assertEqual(str(result), '7 min read')
