# -*- coding: utf-8 -*-

import random
import database

"""

PREPARE:
1) Read text
2) Parse tokens
3) Save to DB

DB:

pairs:
start
end
probability
type (maybe token is not a simple word/comma/dot/dash/etc or 2-3-4-word sequence)

starts:
token

ends:
token

GENERATE:
1) Init sequence with token from starts
2) While token has ends:
    - get ends for token
    - select token from ends (according to probability)
    - append token to sequence
3) Return sequence

"""

def get_random_pair(data, count):
    index = random.randint(0, count - 1)
    start_value, stop_value = 0, 0
    for obj in data:
        stop_value += obj[2]
        if start_value <= index and index < stop_value:
            return obj
        start_value += obj[2]

def generate_sequence():
    """Function for generating sentences"""
    start = database.get_start_token()
    if not start:
        return ''
    data, count = database.get_pairs_for_start(start)
    tokens_list = []
    get_random_pair(data, count)


def main():
    """Main function"""
    random.seed()
    database.init_db()
    generate_sequence()

#Now call main function
main()
