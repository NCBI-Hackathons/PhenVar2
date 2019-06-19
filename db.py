import sqlite3

def connect(db):
    conn = sqlite3.connect(db)

def create_tables(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS publications (id INTEGER PRIMARY KEY, title TEXT, abstract TEXT, FOREIGN KEY (id) REFERENCES snps (rsid))''')
    c.execute('''CREATE TABLE IF NOT EXISTS snps (rsid INTEGER PRIMARY KEY, publication_id INTEGER, FOREIGN KEY (publication_id) REFERENCES publications (id))''')
    conn.commit()
    return()

def add_snp(conn, rsid, publication_id):
    c = conn.cursor()
    c.execute("INSERT INTO snps VALUES (?, ?)", (rsid, publication_id))
    conn.commit()
    return()

def add_publication(conn, id, title, abstract):
    c = conn.cursor()
    c.execute("INSERT INTO publications VALUES (?, ?, ?)", (id, title, abstract))
    conn.commit()
    return()

def close(conn):
    conn.close()
    return()
