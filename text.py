# -*- coding: utf-8 -*-

import re
import database as db

# PREPARE:
# 1) Read text
# 2) Parse tokens
# 3) Save to DB

ENDINGS_RE = "[!.?\n]"
N = 1 #TODO: use different sizes^ trigrams, digrams, single words etc

def read_text(path):
    """Read and parse text file"""
    with open(path, 'r', encoding='utf-8') as f: #read file
        read_data = f.read()
        senteces = re.split(ENDINGS_RE, read_data) #split line by senteces
        for sentece in senteces:
            tokens = parse_tokens(sentece, N) #parse each sentece
            save_to_db(tokens)

def parse_tokens(text, size):
    """Parse sentece and return tokens"""
    words = re.findall(r"\w+|[^\w\s]", text, re.UNICODE) #parse sentece into tokens
    if not words: #empty sentece
        return {}
    for i in range(0, len(words), 2):
        print(words[i])
    return {}

def save_to_db(tokens):
    """Save tokens into database"""
    pass


read_text('test.txt')
