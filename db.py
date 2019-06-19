import sqlite3

def connect(db):
    conn = sqlite3.connect(db)
    return(conn)

def create_tables(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS publications (id INTEGER PRIMARY KEY, title TEXT, abstract TEXT, FOREIGN KEY (id) REFERENCES snps_publications (rsid))''')
    c.execute('''CREATE TABLE IF NOT EXISTS snps_publications (rsid INTEGER, publication_id INTEGER, FOREIGN KEY (publication_id) REFERENCES publications (id), UNIQUE(rsid, publication_id))''')
    conn.commit()
    return()

def add_snp(conn, rsid, publication_id):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO snps_publications VALUES (?, ?)", (rsid, publication_id))
    conn.commit()
    return()

def add_publication(conn, id, title, abstract):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO publications VALUES (?, ?, ?)", (id, title, abstract))
    conn.commit()
    return()

def check_publication(conn, id):
    c = conn.cursor()
    c.execute("SELECT rowid FROM publications WHERE id = ?", (id,))
    if len(c.fetchall()) == 0:
        return(False)
    else:
        return(True)

def close(conn):
    conn.close()
    return()
