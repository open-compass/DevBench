import unittest
from readtime.api import of_text,of_html,of_markdown


class BaseTestCase(unittest.TestCase):
    def test_custom_wpm(self):
        """
        Test case for custom wpm.
        """
        text = 'some test content ' * 100
        result = of_text(text)
        self.assertEqual(result.wpm, 265)
        self.assertEqual(result.seconds, 68)
        self.assertEqual(result.text, '2 min')
        wpm = 50
        result = of_text(text, wpm=wpm)
        self.assertEqual(result.wpm, wpm)
        self.assertEqual(result.seconds, 360)
        self.assertEqual(type(result.seconds), int)
        self.assertEqual(result.text, '6 min')
        self.assertEqual(str(result), '6 min read')

    def test_custom_wpm_html(self):
        html_content = '<p>' + ('some test content ' * 100) + '</p>'
        result = of_html(html_content)
        self.assertEqual(result.wpm, 265)
        wpm = 50
        result = of_html(html_content, wpm=wpm)
        self.assertEqual(result.wpm, wpm)

    def test_custom_wpm_markdown(self):
        markdown_content = '# Title\n' + ('some test content\n' * 100)
        result = of_markdown(markdown_content)
        self.assertEqual(result.wpm, 265)
        wpm = 50
        result = of_markdown(markdown_content, wpm=wpm)
        self.assertEqual(result.wpm, wpm)
