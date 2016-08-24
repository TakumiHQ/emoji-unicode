# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys


CODE_POINTS = '{{code_points}}'  # Template string
NARROW = sys.maxunicode == 0xFFFF

TXT_VARIATION = '\uFE0E'
EMO_VARIATION = '\uFE0F'
KC_MODIFIER = '\u20E3'
ZWJ = '\u200D'
if NARROW:
    FLAGS = '\ud83c[\udde6-\uddff]'
    FITZ_MODIFIER = '\ud83c[\udffb-\udfff]'
else:
    FLAGS = '\U0001F1E6-\U0001F1FF'
    FITZ_MODIFIER = '\U0001F3FB-\U0001F3FF'
KEY_CAPS = '0-9\*#'

RE_PATTERN_TEMPLATE = (
    r'(?P<emoji>'
        r'(?:'
            r'(?:[%(key_caps)s](?:%(emo_variation)s)?%(kc_modifier)s)'
            r'|'
            r'(?:[%(flags)s]){2}'
            r'|'
            r'(?:[%(emojis)s])(?!%(txt_variation)s)'
        r')'
        r'(?:'
            r'(?:(?:%(emo_variation)s)?(?:[%(fitz_modifier)s]))'  # fitzpatrick modifier
            r'|'
            r'(?:(?:%(emo_variation)s)?(?:[%(zwj)s])(?:.)){1,4}'  # Multi glyphs (up to 4)
            r'|'
            r'(?:%(emo_variation)s)'  # Emoji variation
        r')?'
    r')'
) % {
    'emojis': CODE_POINTS,
    'txt_variation': TXT_VARIATION,
    'emo_variation': EMO_VARIATION,
    'fitz_modifier': FITZ_MODIFIER,
    'zwj': ZWJ,
    'flags': FLAGS,
    'kc_modifier': KC_MODIFIER,
    'key_caps': KEY_CAPS
}  # noqa
