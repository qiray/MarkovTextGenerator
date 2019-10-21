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

import sys
import random
import re
import argparse
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK data. Please wait.")
    nltk.download('punkt')

import database
import text

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_BUILD = 4

#TODO: https://github.com/pyinstaller/pyinstaller-hooks and https://pyinstaller.readthedocs.io/en/stable/hooks.html + update version, readme and make release. Improve dabase (make it smaller and/or faster).

def get_version():
    '''Get app version'''
    return "{}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)

def get_random_pair(data, count):
    '''Get random token from pairs according to probability'''
    index = random.randint(0, count - 1)
    start_value, stop_value = 0, 0
    for obj in data:
        stop_value += obj[4]
        if start_value <= index and index < stop_value:
            return obj
        start_value += obj[4]
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

def generate_sequence(number, differentsource):
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
    if differentsource and len(set(sources)) == 1: #if we used only 1 source
        return generate_sequence(number, differentsource) #try to generate another one
    result = list_to_sentence(tokens_list)
    return result

def parse_args():
    """argparse settings"""
    parser = argparse.ArgumentParser(prog='MarkovTextGenerator', description='Markov text generator v {}'.format(get_version()))
    parser.add_argument('--init', action='store_true', help='Init database only')
    parser.add_argument('-f', '--parse', help='Parse text file and save it in database')
    parser.add_argument("-n", "--number", help='Set size of token for text parsing (default = {})'.format(text.N), type=int)
    parser.add_argument("-g", "--generate", help='Generate text sequence', action='store_true')
    parser.add_argument("-v", "--version", help='Show version', action='store_true')
    parser.add_argument("--differentsource", help='Enable this option to generate texts from different sources only', action='store_true')
    return parser, parser.parse_args()

def main():
    """Main function"""
    random.seed()

    try:
        parser, args = parse_args() #parse command line arguments
        if args.init:
            database.init_db()
        if args.number:
            text.set_n_value(args.number)
        if args.parse:
            text.read_text(args.parse)
        if args.generate:
            sentence = generate_sequence(text.N, args.differentsource)
            print(sentence)
        if args.version:
            print("Markov text generator v {}".format(get_version()))
        if len(sys.argv) < 2:
            parser.print_help()
    except FileNotFoundError:
        print("Can't read data file {}".format(args.parse))

#Now call main function
main()
