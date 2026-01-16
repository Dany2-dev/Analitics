import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('storage/users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def create_user(email, password):
    try:
        conn = sqlite3.connect('storage/users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def verify_user(email, password):
    conn = sqlite3.connect('storage/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()
    return user is not None