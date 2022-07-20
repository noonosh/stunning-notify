import sqlite3
import os
import time

DB_NAME = 'notify.db'
ROOT_DIR = os.path.dirname(os.path.abspath('bot.py'))
DB_PATH = os.path.join(ROOT_DIR, DB_NAME)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


def exec(query):
    cursor.execute(query)
    conn.commit()


def create_table():
    exec("CREATE TABLE IF NOT EXISTS groups (group_id INTEGER, name VARCHAR(255), date_added INTEGER)")


def add_group(group_id: int, name: str):
    exec(
        f'INSERT INTO groups (group_id, name, date_added) VALUES (group_id = {group_id}, name = "{name}", date_added = {int(time.time())})')


def get_group(group_id: int):
    q = cursor.execute(f"SELECT * FROM groups WHERE group_id = {group_id}")
    return q.fetchall()
