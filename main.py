# -*- coding: utf-8 -*-

import random
import re
import argparse

import database
import text

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 1

def get_version():
    return "{}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)

def get_random_pair(data, count):
    index = random.randint(0, count - 1)
    start_value, stop_value = 0, 0
    for obj in data:
        stop_value += obj[2]
        if start_value <= index and index < stop_value:
            return obj
        start_value += obj[2]
    return ['', '', 0]

def list_to_sentence(tokens_list):
    result = ' '.join(tokens_list)
    result = result.replace(text.STRING_START_TEXT, '')
    result = re.sub(r'\s+', ' ', result).strip() #remove multiple spaces
    result = re.sub(r'\s([.,!?:)/])', r'\g<1>', result).strip()
    #TODO: check punctuation etc
    return result

def get_pair_for_start(start):
    data, count = database.get_pairs_for_start(start)
    return get_random_pair(data, count)

def generate_sequence():
    """Function for generating sentences"""
    start = database.get_start_token()
    if not start:
        return ''
    pair = get_pair_for_start(start) #get all pairs for selected start
    tokens_list = [pair[0], pair[1]]
    while not database.is_pair_end(pair): #while chosen pair is not end
        pair = get_pair_for_start(pair[1]) # get another list of pairs
        tokens_list.append(pair[1])
    return list_to_sentence(tokens_list)

def parse_args():
    """argparse settings"""
    parser = argparse.ArgumentParser(prog='MarkovTextGenerator', description='Markov text generator v {}'.format(get_version()))
    parser.add_argument('--init', action='store_true', help='Init database only')
    parser.add_argument('-f', '--parse', help='Parse text file and save it in database')
    parser.add_argument("-n", "--number", help='Set size of token for text parsing (default = {})'.format(text.N), type=int)
    parser.add_argument("-g", "--generate", help='Generate text sequence', action='store_true')
    parser.add_argument("-v", "--version", help='Show version', action='store_true')
    return parser.parse_args()

def main():
    """Main function"""
    random.seed()

    args = parse_args() #parse command line arguments
    if args.init:
        database.init_db()
    if args.number:
        text.set_n_value(args.number)
    if args.parse:
        text.read_text(args.parse)
    if args.generate:
        sentence = generate_sequence()
        print(sentence)
    if args.version:
        print("Markov text generator v {}".format(get_version()))

#Now call main function
main()
