# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# This script is base on:
# http://www.unicode.org/Public/emoji/latest/emoji-data.txt
# and (Unicode 8.0 emojis)
# http://unicode.org/reports/tr51/

# Invisible variation selectors:
# U+FE0E for a text presentation
# U+FE0F for an emoji presentation
#
# U+200D ZERO WIDTH JOINER (ZWJ) can be used between the elements
# of a sequence of characters to indicate that a single glyph
# should be presented if available.
#
# EMOJI MODIFIER FITZPATRICK
# U+1F3FB..U+1F3FF
#
# Variation selector (U+FE0F) may or may not be between Fitz modifier and the emoji
#
# Regional indicators:
# 1F1E6..1F1FF
#
# Mark modifiers (ie: square-digits)
# 20E0 enclosing_circle_backlash
# 20E3 enclosing_keycap
#
# emoji sequence:
# (emoji_modifier_base | emoji_base_variation_sequence) | emoji_modifier
#
# emoji core sequence:
# emoji_modifier_base | emoji_base_variation_sequence | emoji_modifier | emoji_flag_sequence

import os
import io
import sys

from .utils import code_point_to_unicode, code_point_to_narrow_unicode

SKIP = [  # Skip lines from emoji-data starting with these
    u'0023',  # Number sign (#)
    u'002A',  # Asterisk (*)
    u'0030',  # Digit zero (0) and up to digit nine (9)
]
DIR = os.path.dirname(__file__)
NARROW = sys.maxunicode == 0xFFFF


def escape_unicode(txt):
    return txt \
        .encode('unicode_escape') \
        .replace(b'\\', b'\\\\') \
        .decode('unicode_escape')


def _parse(line):
    code_point = line.split(';', 1)[0]
    return '-'.join(
        code_point_to_unicode(c)
        for c in code_point.strip().split('..')
    )


def parse():
    with io.open(os.path.join(DIR, 'emoji-data.txt'), mode='r', encoding='utf-8') as fh:
        return [
            _parse(line)
            for line in fh.readlines()
            if (not line.startswith('#')
                and len(line.strip())
                and line[:4] not in SKIP)
        ]

def parse_narrow():
    with io.open(os.path.join(DIR, 'emoji-data.txt'), mode='r', encoding='utf-8') as fh:
        point_dict = dict()
        result = ''
        for line in fh.readlines():
            if (line.startswith('#') or len(line.strip()) == 0 or line[:4] in SKIP):
                continue
            code_point = line.split(';', 1)[0]
            split = code_point.strip().split('..')
            if len(split) == 1:
                # Single code point
                uni = code_point_to_narrow_unicode(split[0])
                if len(uni) == 1:
                    # Code point fits into single narrow unicode character
                    result += uni[0]
                elif len(uni) == 2:
                    val = point_dict.get(uni[0], '')
                    point_dict[uni[0]] = val + uni[1]
                else:
                    raise Exception('1')
            else:
                # Range of code points
                first = code_point_to_narrow_unicode(split[0])
                second = code_point_to_narrow_unicode(split[1])
                if len(first) == 1 and len(second) == 1:
                    # Range is from single narrow to another single narrow unicode
                    result += '{}-{}'.format(first[0], second[0])
                else:
                    # Range from and to surrogates
                    if first[0] == second[0]:
                        val = point_dict.get(first[0], '')
                        point_dict[first[0]] = val + '{}-{}'.format(first[1], second[1])
                    else:
                        raise Exception('Don\'t know how to handle {} for narrow build'.format(line))
        for key in point_dict:
            result += '|{}[{}]'.format(key, ''.join(point_dict[key]))
        return result


def read_template():
    with io.open(os.path.join(DIR, 'pattern_template.py'), mode='r', encoding='utf-8') as fh:
        return fh.read()


def render_template(template, code_points):
    code_points = escape_unicode(''.join(code_points))
    return template.replace('{{code_points}}', code_points)


def write_pattern_file(template_rendered):
    if NARROW:
        with io.open(os.path.join(DIR, 'pattern_narrow.py'), mode='w', encoding='utf-8') as fh:
            fh.write(template_rendered)
    else:
        with io.open(os.path.join(DIR, 'pattern.py'), mode='w', encoding='utf-8') as fh:
            fh.write(template_rendered)


def generate_pattern_file():
    if NARROW:
        code_points = parse_narrow()
    else:
        code_points = parse()
    template = read_template()
    template_rendered = render_template(template, code_points)
    write_pattern_file(template_rendered)


