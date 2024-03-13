"""
    readtime.api
    ~~~~~~~~~~~~

    Contains public methods.

    :copyright: (c) 2016 Alan Hamlett.
    :license: BSD, see LICENSE for more details.
"""


from . import utils


def of_text(text, wpm=265):
    """
    Calculate the reading time of a given text.

    Parameters:
        text (str): The text to calculate the reading time for.
        wpm (int, optional): The reading speed in words per minute. Defaults to None.

    Returns:
        float: The estimated reading time in minutes.
    """
    return utils.read_time(text, format='text', wpm=wpm)


def of_html(html, wpm=265):
    """
    Calculate the reading time of an HTML document.

    Parameters:
        html (str): The HTML document to calculate the reading time for.
        wpm (int, optional): The reading speed in words per minute. Defaults to None.

    Returns:
        float: The estimated reading time in minutes.
    """
    return utils.read_time(html, format='html', wpm=wpm)


def of_markdown(markdown, wpm=265):
    """
    Calculate the reading time of a markdown text.

    Parameters:
        markdown (str): The markdown text to calculate the reading time for.
        wpm (int, optional): The reading speed in words per minute. Defaults to None.

    Returns:
        float: The estimated reading time in minutes.
    """
    return utils.read_time(markdown, format='markdown', wpm=wpm)
