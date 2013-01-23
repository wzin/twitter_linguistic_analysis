# -*- coding: utf-8 -*-
def pl_to_ang(text):
    translate = {u'ą':'a', u'ć':'c', u'ę':'e', u'ł':'l', u'ń':'n', u'ó':'o', u'ś':'s', u'ż':'z', u'ź':'z'}
    newText = ''
    for c in text:
        if c in translate:
            c = translate[c]
        elif c in [x.upper() for x in translate.keys()]:
            c = translate[c.lower()].upper()
        newText = newText + c
    return newText
