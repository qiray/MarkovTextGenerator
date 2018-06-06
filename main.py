# -*- coding: utf-8 -*-

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

def generate_sequence():
    """TODO: wrtie"""
    pass

def main():
    """TODO: write usage"""
    pass

#Now call main function
main()
