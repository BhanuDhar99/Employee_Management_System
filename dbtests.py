import sqlite3


with sqlite3.connect('ems.db') as con:
    cur = con.cursor()
    cur.execute('''SELECT*FROM UserProjectInfo''')

    rows = cur.fetchall()
    for row in rows:
        print(row)

