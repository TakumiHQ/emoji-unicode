# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def code_point_to_unicode(code_point):
    try:
        return unichr(int(code_point, 16))
    except NameError:
        return chr(int(code_point, 16))


def code_point_to_narrow_unicode(code_point):
    val = '\\U{:08x}'.format(int(code_point, 16))
    uni = val.decode('unicode-escape')
    return list(uni)


def unicode_to_code_point(uni_char):
    return format(ord(uni_char), 'x').lower()
