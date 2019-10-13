import sqlite3

'''admin_email='e'
with sqlite3.connect('ems.db') as con:
    cur = con.cursor()
    #cur.execute('''#SELECT*FROM AdminInfo''')

''' rows = cur.fetchall()
    for row in rows:
        print(row)
''' 

cursor = ems.execute('''SELECT*FROM AdminInfo''')
print(cursor.fetchall())
