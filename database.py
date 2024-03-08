import sqlite3
from flask import g

DATABASE = 'inventory.db'

# Fungsi untuk mendapatkan koneksi ke database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Fungsi untuk inisialisasi database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('PRAGMA foreign_keys = ON')
        with open('schema.sql', 'r') as f:
            schema = f.read()
        conn.executescript(schema)
