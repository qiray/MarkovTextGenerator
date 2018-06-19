# -*- coding: utf-8 -*-
'''database module'''

import sqlite3

DBFILE = 'data.db'

def init_db():
    """init database"""
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS pairs (
            begin TEXT,
            end TEXT,
            count INTEGER DEFAULT 0,
            PRIMARY KEY (begin, end)
        );
        CREATE TABLE IF NOT EXISTS begins (
            token TEXT PRIMARY KEY
        );
        CREATE TABLE IF NOT EXISTS ends (
            token TEXT PRIMARY KEY
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

def save_tokens(tokens, cursor):
    """Save tokens into opened database\n
    start_connection() should be called before this function
    end_connecion() should be called after saving all tokens
    """
    #https://stackoverflow.com/questions/1711631/improve-insert-per-second-performance-of-sqlite
    for token in tokens:
        cursor.execute('''
            INSERT OR IGNORE INTO pairs(
                begin,
                end
            ) VALUES(?, ?);
        ''', (token.begin, token.end))
        cursor.execute('UPDATE pairs SET count = count + 1 WHERE begin = ? AND end = ?;',
                       (token.begin, token.end))
        if token.is_begin == 1:
            cursor.execute('INSERT OR IGNORE INTO begins(token) VALUES(?)', (token.begin,))
        if token.is_end == 1:
            cursor.execute('INSERT OR IGNORE INTO ends(token) VALUES(?)', (token.end,))

def get_start_token():
    """Return random start token from database"""
    conn, cursor = start_connection()
    cursor.execute('''SELECT * from pairs INNER JOIN begins ON pairs.begin = begins.token
                   ORDER BY RANDOM() LIMIT 1;''')
    result = cursor.fetchall()
    end_connecion(conn)
    return result

def get_pairs_for_start(start):
    """Return all pairs from database for chosen start token"""
    conn, cursor = start_connection()
    cursor.execute('SELECT * from pairs WHERE begin = ?;', (start,))
    result = cursor.fetchall()
    end_connecion(conn)
    return result
