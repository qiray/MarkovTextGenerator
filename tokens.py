# -*- coding: utf-8 -*-

# Copyright (c) 2018-2019, Yaroslav Zotov, https://github.com/qiray/
# All rights reserved.

# This file is part of MarkovTextGenerator.

# MarkovTextGenerator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# MarkovTextGenerator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with MarkovTextGenerator.  If not, see <https://www.gnu.org/licenses/>.

class Token(object):

    def __init__(self, begin, end, source=1, is_begin=0, is_end=0):
        self.begin = begin
        self.end = end
        self.is_begin = is_begin
        self.is_end = is_end
        self.source = source

    def __str__(self):
        return self.begin + ' --- ' + self.end + ' (%d %d)' % (self.is_begin, self.is_end)
