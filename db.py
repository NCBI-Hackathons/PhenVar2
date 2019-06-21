from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import Index
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import create_engine, select

Base = declarative_base()

class Publication(Base):
    __tablename__ = 'publication'
    id = Column(Integer, primary_key = True)
    title = Column(String(250))
    abstract = Column(String(250))
    # rsids = Column(Integer)

class Snp(Base):
    __tablename__ = 'snp_publications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rsid = Column(Integer)
    publications = Column(Integer, ForeignKey('publication.id'))

def create(database):
    # an engine that the session will use for resources
    engine = create_engine(database)
    # create a configured Session class
    Session = sessionmaker(bind=engine)
    # create a session
    session = Session()
    return engine, session

def connect(engine):
    conn = engine.connect()
    return conn

def create_tables(engine):
    Base.metadata.create_all(engine)
    return()

def add_snp(session, rsid, publication_id):
    snp = Snp(rsid = rsid, publications = publication_id)
    print("Adding snp: ", rsid, "|", publication_id)
    session.add(snp)
    session.commit()
    return()

def add_publication(session, id, title, abstract):
    publication = Publication(id = id, title = title, abstract = abstract)
    print("Adding publication: ", id, "|", title, "|", abstract)
    session.add(publication)
    session.commit()
    return()

def check_publication(session, id):
    publication = session.query(Publication).filter_by(id=id).scalar()
    if publication == None:
        return(False)
    return(True)

def check_snp(session, id, pub):
    snp = session.query(Snp).filter_by(rsid=id).filter_by(publications=pub).scalar()
    if snp == None:
        return(False)
    return(True)

def check_snp_duplicates(session, id, pub):
    entries = session.query(Snp).filter_by(rsid=id).filter_by(publications=pub).count()
    return(entries)

def all_filtered_snps(session, id, pub):
    query = session.query(Snp).filter_by(rsid=id).filter_by(publications=pub)
    rows = query.all()
    return(rows)

def get_snp_rows(session):
    query = session.query(Snp)
    rows = query.all()
    return(rows)

def result_dict(r):
    return dict(zip(r.keys(), r))

def result_dicts(rs):
    return list(map(result_dict, rs))

def table_dump(session, table):
    if table == 'publication':
        stmt = select('*').select_from(Publication)
    elif table == 'snp':
        stmt = select('*').select_from(Snp)
    result = session.execute(stmt).fetchall()
    print(result_dicts(result))
    return()


def close(conn):
    conn.close()
    return()
