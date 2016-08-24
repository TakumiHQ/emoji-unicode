# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys


CODE_POINTS = '\xa9\xae\u203c\u2049\u2122\u2139\u2194-\u2199\u21a9-\u21aa\u231a-\u231b\u2328\u23cf\u23e9-\u23f3\u23f8-\u23fa\u24c2\u25aa-\u25ab\u25b6\u25c0\u25fb-\u25fe\u2600-\u2604\u260e\u2611\u2614-\u2615\u2618\u261d\u2620\u2622-\u2623\u2626\u262a\u262e-\u262f\u2638-\u263a\u2648-\u2653\u2660\u2663\u2665-\u2666\u2668\u267b\u267f\u2692-\u2694\u2696-\u2697\u2699\u269b-\u269c\u26a0-\u26a1\u26aa-\u26ab\u26b0-\u26b1\u26bd-\u26be\u26c4-\u26c5\u26c8\u26ce\u26cf\u26d1\u26d3-\u26d4\u26e9-\u26ea\u26f0-\u26f5\u26f7-\u26fa\u26fd\u2702\u2705\u2708-\u2709\u270a-\u270b\u270c-\u270d\u270f\u2712\u2714\u2716\u271d\u2721\u2728\u2733-\u2734\u2744\u2747\u274c\u274e\u2753-\u2755\u2757\u2763-\u2764\u2795-\u2797\u27a1\u27b0\u27bf\u2934-\u2935\u2b05-\u2b07\u2b1b-\u2b1c\u2b50\u2b55\u3030\u303d\u3297\u3299|\ud83d[\udc00-\udc3e\udc3f\udc40\udc41\udc42-\udcf7\udcf8\udcf9-\udcfc\udcfd\udcff\udd00-\udd3d\udd49-\udd4a\udd4b-\udd4e\udd50-\udd67\udd6f-\udd70\udd73-\udd79\udd7a\udd87\udd8a-\udd8d\udd90\udd95-\udd96\udda4\udda5\udda8\uddb1-\uddb2\uddbc\uddc2-\uddc4\uddd1-\uddd3\udddc-\uddde\udde1\udde3\udde8\uddef\uddf3\uddfa\uddfb-\uddff\ude00\ude01-\ude10\ude11\ude12-\ude14\ude15\ude16\ude17\ude18\ude19\ude1a\ude1b\ude1c-\ude1e\ude1f\ude20-\ude25\ude26-\ude27\ude28-\ude2b\ude2c\ude2d\ude2e-\ude2f\ude30-\ude33\ude34\ude35-\ude40\ude41-\ude42\ude43-\ude44\ude45-\ude4f\ude80-\udec5\udecb-\udecf\uded0\uded1-\uded2\udee0-\udee5\udee9\udeeb-\udeec\udef0\udef3\udef4-\udef6]|\ud83c[\udc04\udccf\udd70-\udd71\udd7e\udd7f\udd8e\udd91-\udd9a\udde6-\uddff\ude01-\ude02\ude1a\ude2f\ude32-\ude3a\ude50-\ude51\udf00-\udf20\udf21\udf24-\udf2c\udf2d-\udf2f\udf30-\udf35\udf36\udf37-\udf7c\udf7d\udf7e-\udf7f\udf80-\udf93\udf96-\udf97\udf99-\udf9b\udf9e-\udf9f\udfa0-\udfc4\udfc5\udfc6-\udfca\udfcb-\udfce\udfcf-\udfd3\udfd4-\udfdf\udfe0-\udff0\udff3-\udff5\udff7\udff8-\udfff]|\ud83e[\udd10-\udd18\udd19-\udd1e\udd20-\udd27\udd30\udd33-\udd3a\udd3c-\udd3e\udd40-\udd45\udd47-\udd4b\udd50-\udd5e\udd80-\udd84\udd85-\udd91\uddc0]'  # Template string
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
