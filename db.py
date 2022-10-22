import sqlite3

from matplotlib.backend_bases import cursors

conn = sqlite3.connect("playerwins.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE playerwins (
    player varchar(64) PRIMARY KEY,
    wins integer NOT NULL
)"""
cursor.execute(sql_query)

for i in ["Player1", "Player2"]:
    cursor.execute("""INSERT into playerwins VALUES (?, ?)""", (i, 0))

conn.commit()