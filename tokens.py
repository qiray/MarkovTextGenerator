# -*- coding: utf-8 -*-

class Token(object):

    def __init__(self, begin, end, source='', is_begin=0, is_end=0):
        self.begin = begin
        self.end = end
        self.is_begin = is_begin
        self.is_end = is_end
        self.source = source

    def __str__(self):
        return self.begin + ' --- ' + self.end + ' (%d %d)' % (self.is_begin, self.is_end)
