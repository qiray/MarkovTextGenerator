# -*- coding: utf-8 -*-

class Token(object):

    def __init__(self, begin, end, is_begin, is_end):
        self.begin = begin
        self.end = end
        self.is_begin = is_begin
        self.is_end = is_end

    def func(self, param):
        if param:
            pass
