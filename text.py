# -*- coding: utf-8 -*-
'''This module is used for preparing database with text data'''

import re
import nltk #for text parsing
import database as db
import tokens

# PREPARE:
# 1) Read text
# 2) Parse tokens
# 3) Save to DB

def read_text(path):
    """Read and parse text file"""
    db.init_db() #init database to prevent bad situations
    with open(path, 'r', encoding='utf-8') as f: #read file
        read_data = f.read()
        #sentences = re.findall(r'[^!.?\n]*[.?!\n]+(?=[ \n])', read_data) #split line by sentences
        sentences = nltk.sent_tokenize(read_data) #use nltk to parse text into sentences
        conn, cursor = db.start_connection()
        for sentence in sentences:
            current_tokens = parse_tokens(sentence) #parse each sentence
            db.save_tokens(current_tokens, cursor)
        db.end_connecion(conn)

def parse_tokens(text):
    """Parse sentence and return tokens"""
    text = re.sub(r'\s+', ' ', text).strip() #remove multiple spaces

    # words = re.findall(r"[\w-]+|[^\w\s]", text, re.UNICODE) #parse sentence into tokens
    words = nltk.word_tokenize(text) #parse sentence into tokens
    # words = re.findall(r"\w+\s*|[^\w\s]\s*", text, re.UNICODE) #with spaces
    if not words: #empty sentence
        return []
    length = len(words)
    result = []
    for i in range(0, length):
        is_begin = 1 if i == 0 else 0
        is_end = 1 if i + 1 >= length - 1 else 0
        start = words[i] if i < length else ''
        end = words[i + 1] if i + 1 < length else ''
        token = tokens.Token(start, end, is_begin, is_end)
        result.append(token)
    return result
