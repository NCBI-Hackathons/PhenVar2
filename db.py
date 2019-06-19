import sqlite3

conn = sqlite3.connect("phenvar.db")

def createTables(conn):
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS publications (id INTEGER PRIMARY KEY, title TEXT, abstract TEXT, FOREIGN KEY (id) REFERENCES snps (rsid))''')
    c.execute('''CREATE TABLE IF NOT EXISTS snps (rsid INTEGER PRIMARY KEY, publication_id INTEGER, FOREIGN KEY (publication_id) REFERENCES publications (id))''')

def addSnpsRow(conn, rsid, publication_id):
    c = conn.cursor()

    c.execute("INSERT INTO snps VALUES (?, ?)", (rsid, publication_id))

def addPublicationsRow(conn, id, title, abstract):
    c = conn.cursor()

    c.execute("INSERT INTO publications VALUES (?, ?, ?)", (id, title, abstract))


#createTables(conn)
conn.commit()
conn.close()
