import sqlite3

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS datamap')
c.execute('''CREATE TABLE datamap
          (key text, sheet text, cell_ref text)''')
c.execute("INSERT INTO datamap VALUES ('Programme/Project Name','Summary','B5')")
c.execute("INSERT INTO datamap VALUES ('SRO-Sign-Off','Summary','C7')")
c.execute("INSERT INTO datamap VALUES ('PD Full Name','Summary','D7')")

# conn = sqlite3.connect('db.sqlite')
# for row in c.execute('SELECT * FROM datamap'):
#     print(row)
conn.commit()
conn.close()
