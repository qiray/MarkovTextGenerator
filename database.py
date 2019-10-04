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

'''database module'''

import sqlite3

import text

DBFILE = 'data.db'

def init_db():
    """init database"""
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS pairs (
            begin TEXT,
            end TEXT,
            is_begin INTEGER,
            is_end INTEGER,
            count INTEGER DEFAULT 0,
            size INTEGER,
            source INTEGER,
            PRIMARY KEY (begin, end)
        );
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER AUTO INCREMENT PRIMARY KEY,
            name text
        );
    """)
    conn.commit()
    conn.close()

def start_connection():
    """Open database and return connection with cursor to it"""
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    return conn, cursor

def end_connecion(conn):
    """Commit and close connection to database"""
    conn.commit()
    conn.close()

def save_source(source_name):
    conn, cursor = start_connection()
    cursor.execute('INSERT OR IGNORE INTO sources (name) VALUES(?);', (source_name,))
    cursor.execute('SELECT last_insert_rowid() FROM sources;')
    result = cursor.fetchone()
    end_connecion(conn)
    return result[0] if result else 1

def save_tokens(tokens, cursor, number=1):
    """Save tokens into opened database\n
    start_connection() should be called before this function
    end_connecion() should be called after saving all tokens
    """
    #https://stackoverflow.com/questions/1711631/improve-insert-per-second-performance-of-sqlite
    for token in tokens:
        cursor.execute('''
            INSERT OR IGNORE INTO pairs(
                begin,
                end,
                is_begin,
                is_end,
                size,
                source
            ) VALUES(?, ?, ?, ?, ?, ?);
        ''', (token.begin, token.end, token.is_begin, token.is_end, number, token.source))
        cursor.execute('UPDATE pairs SET count = count + 1 WHERE begin = ? AND end = ? AND size = ?;',
                       (token.begin, token.end, number))

def get_start_token():
    """Return random start token from database"""
    conn, cursor = start_connection()
    cursor.execute('SELECT * from pairs WHERE is_begin = 1 ORDER BY RANDOM() LIMIT 1;')
    result = cursor.fetchone()
    end_connecion(conn)
    return result[0] if result else ''

def get_pairs_for_list(tokens_list, number):
    """Return all pairs from database for chosen start token"""
    start = tokens_list[-1]
    conn, cursor = start_connection()
    cursor.execute('SELECT * from pairs WHERE begin = ?;', (start,))
    result = cursor.fetchall()
    if not result:
        start = ' '.join(text.split_into_words(' '.join(tokens_list))[-number:])
        cursor.execute('SELECT * from pairs WHERE begin = ?;', (start,))
        result = cursor.fetchall()
    cursor.execute('SELECT SUM(count) from pairs WHERE begin = ?;', (start,))
    count = cursor.fetchone()
    end_connecion(conn)
    if not result:
        return [], 0
    return result, count[0] if count else 0

def is_pair_end(pair):
    '''Return true when pair is end'''
    conn, cursor = start_connection()
    cursor.execute('SELECT * from pairs WHERE is_end = 1 AND (end = ? OR end = ?);', (pair[0], pair[1],))
    result = cursor.fetchone()
    end_connecion(conn)
    return False if not result else True
