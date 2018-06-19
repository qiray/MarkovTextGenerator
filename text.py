# -*- coding: utf-8 -*-
'''This module is used for preparing database with text data'''

import sys
import re
from nltk import sent_tokenize #for text parsing
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
        #sentences = re.findall(r'[^!.?\n]*[.?!\n]+(?=[ \n])', read_data) #split line by sentences
        sentences = sent_tokenize(read_data) #use nltk to parse text into sentences
        conn, cursor = db.start_connection()
        for sentence in sentences:
            current_tokens = parse_tokens(sentence, N) #parse each sentence
            db.save_tokens(current_tokens, cursor)
        db.end_connecion(conn)

def parse_tokens(text, size):
    """Parse sentence and return tokens"""
    text = text.replace(r"\s+", " ") #replace multiple spaces

    string_start = STRING_START_TEXT * (size - 1)
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
        is_begin = 1 if i <= size - 1 else 0
        is_end = 1 if i + size >= length - 1 else 0
        start = ' '.join(lists[i]) if i < length else ''
        end = ' '.join(lists[i + size]) if i + size < length else ''
        token = tokens.Token(start, end, is_begin, is_end)
        result.append(token)
    return result

#read text and parse it
read_text(sys.argv[1] if len(sys.argv) > 1 else 'test.txt')
