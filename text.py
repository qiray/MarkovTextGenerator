# -*- coding: utf-8 -*-

import re
from functools import reduce
import database as db

# PREPARE:
# 1) Read text
# 2) Parse tokens
# 3) Save to DB

N = 2 #used for different sizes - trigrams, digrams etc

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
    words = re.findall(r"[\w-]+|[^\w\s]", text, re.UNICODE) #parse sentence into tokens
    # words = re.findall(r"\w+\s*|[^\w\s]\s*", text, re.UNICODE) #with spaces
    if not words: #empty sentence
        return {}
    length = len(words)
    lists = []
    for i in range(0, length):
        wordlist = []
        for j in range(0, N):
            if i + j < length: #we can append more words
                wordlist.append(words[i + j])
        lists.append(wordlist)
    print(lists)
    return {} #TODO: generate tokens

def save_to_db(tokens):
    """Save tokens into database"""
    sql = ''
    for token in tokens:
        pass
    pass


read_text('test.txt')
