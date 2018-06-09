# -*- coding: utf-8 -*-

import re
from functools import reduce
import database as db
import tokens

# PREPARE:
# 1) Read text
# 2) Parse tokens
# 3) Save to DB

N = 1 #used for different sizes - trigrams, digrams etc
STRING_START_TEXT = 'STRING_START_TOKEN '

def read_text(path):
    """Read and parse text file"""
    with open(path, 'r', encoding='utf-8') as f: #read file
        read_data = f.read()
        sentences = re.findall(r'[^!.?\n]*[.?!]+', read_data) #split line by sentences
        for sentence in sentences:
            tokens = parse_tokens(sentence, N) #parse each sentence
            save_to_db(tokens)

def parse_tokens(text, size):
    """Parse sentence and return tokens"""
    text = text.replace(r"\s+", " ") #replace multiple spaces

    string_start = STRING_START_TEXT * (N - 1) 
    text = string_start + text #append to text some special start tokens

    words = re.findall(r"[\w-]+|[^\w\s]", text, re.UNICODE) #parse sentence into tokens
    # words = re.findall(r"\w+\s*|[^\w\s]\s*", text, re.UNICODE) #with spaces
    if not words: #empty sentence
        return []
    length = len(words)
    lists = []
    for i in range(0, length):
        wordlist = []
        for j in range(0, N):
            if i + j < length: #we can append more words
                wordlist.append(words[i + j])
        lists.append(wordlist)
    result = []
    length = len(lists)
    for i in range(0, length):
        is_begin = 1 if i <= N - 1 else 0
        is_end = 1 if i + N >= length - 1 else 0
        start = ' '.join(lists[i]) if i < length else ''
        end = ' '.join(lists[i + N]) if i + N < length else ''
        token = tokens.Token(start, end, is_begin, is_end)
        result.append(token)
    return result

def save_to_db(tokens):
    """Save tokens into database"""
    sql = ''
    for token in tokens:
        pass
    pass


read_text('test.txt')
