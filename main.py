# -*- coding: utf-8 -*-

import random
import re
import argparse

import database
import text
import twitter

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 3

def get_version():
    '''Get app version'''
    return "{}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)

def get_random_pair(data, count):
    '''Get random token from pairs according to probability'''
    index = random.randint(0, count - 1)
    start_value, stop_value = 0, 0
    for obj in data:
        stop_value += obj[2]
        if start_value <= index and index < stop_value:
            return obj
        start_value += obj[2]
    return ['', '', 0]

def list_to_sentence(tokens_list):
    '''Convert list of tokens to sentence'''
    result = ' '.join(tokens_list)
    result = result.replace(text.STRING_START_TEXT, '')
    result = re.sub(r'\s+', ' ', result).strip() #remove multiple spaces
    result = re.sub(r'\s([.,;!?:)/])', r'\g<1>', result).strip()
    result = re.sub(r'« ', r'«', result).strip()
    result = re.sub(r' »', r'»', result).strip()
    result = re.sub(r'\( ', r'(', result).strip()
    result = re.sub(r'`|"|\[|\]', '', result).strip()
    return result

def get_next_pair(tokens_list, number):
    data, count = database.get_pairs_for_list(tokens_list, number)
    if count <= 0:
        return None
    return get_random_pair(data, count)

def generate_sequence(number):
    """Function for generating sentences"""
    start = database.get_start_token()
    if not start:
        return ''
    tokens_list = [start]
    pair = get_next_pair(tokens_list, number) #get all pairs for selected start
    sources = [pair[4]]
    tokens_list.append(pair[1])
    while not database.is_pair_end(pair): #while chosen pair is not end
        pair = get_next_pair(tokens_list, number) # get another list of pairs
        if not pair:
            break
        sources.append(pair[4]) #save pairs' sources int the list
        tokens_list.append(pair[1])
    if(len(set(sources)) == 1): #if we used only 1 source
        return generate_sequence(number) #try to generate another one
    return list_to_sentence(tokens_list)

def parse_args():
    """argparse settings"""
    parser = argparse.ArgumentParser(prog='MarkovTextGenerator', description='Markov text generator v {}'.format(get_version()))
    parser.add_argument('--init', action='store_true', help='Init database only')
    parser.add_argument('-f', '--parse', help='Parse text file and save it in database')
    parser.add_argument("-n", "--number", help='Set size of token for text parsing (default = {})'.format(text.N), type=int)
    parser.add_argument("-g", "--generate", help='Generate text sequence', action='store_true')
    parser.add_argument("-v", "--version", help='Show version', action='store_true')
    parser.add_argument("-t", "--tweet", help='Post in twitter (you need file secrets.py with Twitter application config)', action='store_true')
    return parser.parse_args()

def main():
    """Main function"""
    random.seed()

    try:
        args = parse_args() #parse command line arguments
        if args.init:
            database.init_db()
        if args.number:
            text.set_n_value(args.number)
        if args.parse:
            text.read_text(args.parse)
        if args.generate:
            sentence = generate_sequence(text.N)
            print(sentence)
            if args.tweet:
                twitter.tweet(sentence)
        if args.version:
            print("Markov text generator v {}".format(get_version()))
    except FileNotFoundError:
        print("Can't read data file {}".format(args.parse))

#Now call main function
main()
