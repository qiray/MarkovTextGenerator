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

'''This module is used for preparing database with text data'''

import re
import nltk #for text parsing
import database as db
import tokens

N = 3 #used for different sizes - trigrams, digrams etc
STRING_START_TEXT = 'STRING_START_TOKEN '

# PREPARE:
# 1) Read text
# 2) Parse tokens
# 3) Save to DB

def set_n_value(number):
    global N
    N = number

def split_into_words(text):
    """Split text into words"""
    words = nltk.word_tokenize(text) #parse sentence into tokens
    return words

def read_text(path):
    """Read and parse text file"""
    db.init_db() #init database to prevent bad situations
    with open(path, 'r', encoding='utf-8') as f: #read file
        read_data = f.read()
        sentences = nltk.sent_tokenize(read_data) #use nltk to parse text into sentences
        source_id = db.save_source(path)
        conn, cursor = db.start_connection()
        for sentence in sentences:
            current_tokens = parse_tokens(sentence, N, source_id) #parse each sentence
            db.save_tokens(current_tokens, cursor, N)
        db.end_connecion(conn)

def parse_tokens(text, size, source_id):
    """Parse sentence and return tokens"""
    text = re.sub(r'\s+', ' ', text).strip() #remove multiple spaces

    string_start = STRING_START_TEXT * (size - 1)
    text = string_start + text #append to text some special start tokens

    words = split_into_words(text)
    if not words: #empty sentence
        return []
    length = len(words)
    lists = []
    for i in range(0, length):
        wordlist = []
        for j in range(0, size):
            if i + j < length: #we can append more words
                wordlist.append(words[i + j])
        lists.append(wordlist)
    result = []
    length = len(lists)
    for i in range(0, length):
        is_begin = 1 if i <= size - 1 else 0
        is_end = 1 if i + size >= length - 1 else 0
        start = ' '.join(lists[i]) if i < length else ''
        end = lists[i + size][0] if i + size < length else ''
        token = tokens.Token(start, end, source_id, is_begin, is_end)
        result.append(token)
    return result
