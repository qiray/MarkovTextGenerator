# -*- coding: utf-8 -*-

import re
import database as db

# PREPARE:
# 1) Read text
# 2) Parse tokens
# 3) Save to DB

ENDINGS_RE = "[!.?\n]"
N = 1 #used for different sizes - trigrams, digrams etc

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
    text = text.replace(r"\s+", " ") #replace multiple spaces
    words = re.findall(r"[\w-]+|[^\w\s]", text, re.UNICODE) #parse sentece into tokens
    # words = re.findall(r"\w+\s*|[^\w\s]\s*", text, re.UNICODE) #with spaces
    if not words: #empty sentece
        return {}
    length = len(words)
    for i in range(0, length):
        wordlist = []
        for j in range(0, N):
            if i + j < length: #we can append more words
                wordlist.append(words[i + j])
        print(wordlist)
        # print(' '.join(wordlist))
    return {}

def save_to_db(tokens):
    """Save tokens into database"""
    sql = ''
    for token in tokens:
        pass
    pass


read_text('test.txt')
