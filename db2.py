import sqlalchemy as db

def create(database):
    engine = db.create_engine(database)
    return engine

def connect(database):
    engine = create(database)
    conn = engine.connect()
    return conn

def create_tables(conn):
    return

def add_snp(conn, rsid, publication_id):
    return

def add_publication(conn, id, title, abstract):
    return

def check_publication(conn, id):
    return

def close(conn):
    conn.engine.close()
    return

