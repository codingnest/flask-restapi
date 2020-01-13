import sqlite3

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

create_users_table = "CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_users_table)

create_items_table = "CREATE TABLE items (name text PRIMARY KEY, price real)"

cursor.execute(create_items_table)

conn.commit()
conn.close()
