# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
import sys

from .models import Emoji, JOINER_CHARS
from .utils import code_point_to_unicode
if sys.maxunicode == 0xFFFF:
    from .pattern_narrow import RE_PATTERN_TEMPLATE
else:
    from .pattern import RE_PATTERN_TEMPLATE

PATTERN = re.compile(RE_PATTERN_TEMPLATE)


def replace(txt, callback):
    """
    Replace all unicode emojis in a given text

    :param str txt: Text source to be parsed
    :param callable callback: A callable that should accept\
    a instance of :py:class:`Emoji` and\
    return a str to replace the match
    :return: Parsed text with all the emojis\
    replaced by the callback result
    :rtype: str
    """
    def func(m):
        return callback(Emoji(unicode=m.group('emoji')))

    return re.sub(PATTERN, func, txt)


def normalize(code_points, separator='-'):
    """
    Normalize a code point removing joiner\
    characters such as emoji variations,\
    Zero Width Joiner and leading zeros

    :param str code_points: code points separated by an hyphen\
    or the separator param value
    :param str separator: The separator used to split the code points,\
    process them and merge them back
    :return: Code points with no joiner chars,\
    leading zeros, and lower cased.
    :rtype: str
    """
    return separator.join(
        c.lstrip('0').lower()
        for c in code_points.split(separator)
        if code_point_to_unicode(c) not in JOINER_CHARS
    )


def get_emojis(txt, ignore_fitzpatrick=False):
    """
    Return a list of all emojis found in the text

    :param str txt: Text source to be parsed
    :param bool ignore_fitzpatrick: Wether to ignore the fitzpatrick\
    skin modifier emojis
    :return: List of all the emojis
    :rtype: list
    """
    return PATTERN.findall(txt)
