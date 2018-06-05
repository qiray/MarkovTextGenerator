# -*- coding: utf-8 -*-

# PREPARE:
# 1) Read text
# 2) Parse tokens
# 3) Save to DB

def read_text(path):
    with open(path, 'r') as f: #read file
        read_data = f.read()
        tokens = parse_tokens(read_data)
        save_to_db(tokens)

def parse_tokens(text):
    return {}

def save_to_db(sql):
    pass
