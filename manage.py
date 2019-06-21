#!/usr/bin/env python3
import db
from phenvar import get_complete_rsids, get_pmids, get_publication
import time
from sys import argv
from sqlalchemy import select


help_text = """USAGE:
./manage.py <command>
 commands:
    - initialize    creates tables in database, should only be run once
    - update_snps   gets rsids and populates database
    - update_publications   gets publications and populates database
    - dump_publication  prints publication table
    - dump_snp  prints snp table
    - remove_duplicates_snps    finds duplicate snp rows and removes them
"""

def help():
    print(help_text)

def initialize():
    # engine, session = db.create("sqlite:///db.sqlite3")
    # db.create_tables(engine)
    update_snps()
    update_publications()
    # db.close(session)

def init_session():
    engine, session = db.create("sqlite:///db.sqlite3")
    db.create_tables(engine)
    return(session)

def dump_publication():
    session = init_session()
    db.table_dump(session, 'publication')
    db.close(session)
    return()

def dump_snp():
    session = init_session()
    db.table_dump(session, 'snp')
    db.close(session)
    return()

def remove_duplicates_snps():
    print("remove_duplicates called")
    session = init_session()
    rows = db.get_snp_rows(session)
    for row in rows:
        # print("row type", type(row))
        # print(row.rsid)
        # print(row.publications)
        entries = db.check_snp_duplicates(session, row.rsid, row.publications)
        if entries > 1:
            print("duplicate found")
            items = db.all_filtered_snps(session, row.rsid, row.publications)
            count = 0
            for item in items:
                # keep the first entry found and delete all others
                if count == 0:
                    count += 1
                else:
                    print("deleting ", item)
                    session.delete(item)
                    session.commit()
                    
        # else:
        #     print("not a duplicate", entries)
    return()

def update_snps():
    session = init_session()
    p_snps = 0
    snps = get_complete_rsids()
    # for each rsid, get pmids
    for s in snps:
        time.sleep(.1)
        pubs = get_pmids(s)
        if len(pubs) > 0:
            p_snps += 1
            print("Processed {} snps".format(p_snps))
            # if entries not in db, add
            for p in pubs:
                if not db.check_snp(session=session, id=s, pub=p):
                    db.add_snp(session, s, p)
                # db.add_snp(session, s, p)
                    # print("snp not in database; adding")
    db.close(session)
    return()

def update_publications():
    session = init_session()
    p_pubs = 0
    # for row in snps_publications get pmid
    rows = db.get_snp_rows(session)
    for row in rows:
        pmid = row.publications
        # check if pmid in db, add if not
        if not db.check_publication(session=session, id=pmid):
            time.sleep(.1)
            info = get_publication(pmid)
            db.add_publication(session, id=pmid, title=info["title"], abstract=info["abstract"])
            # print("publication not in database; adding")
        p_pubs += 1
        print("Processed {} pubs".format(p_pubs))
    db.close(session)
    return()

def old_initialize():
    engine, session = db.create("sqlite:///db.sqlite3")
    db.create_tables(engine)
    p_snps = 0
    p_pubs = 0
    snps = get_complete_rsids()
    for s in snps:
        time.sleep(.1)
        pubs = get_pmids(s)
        if len(pubs) > 0:
            p_snps = p_snps + 1
            print("Processed {} snps".format(p_snps))
            for p in pubs:
                if not db.check_snp(session=session, id=s, pub=p):
                    db.add_snp(session, s, p)
                if not db.check_publication(session=session, id=p):
                    info = get_publication(p)
                    db.add_publication(session, id=p, title=info["title"], abstract=info["abstract"])
                p_pubs = p_pubs + 1
                print("Processed {} pubs".format(p_pubs))
    db.close(session)
    return()


commands = {
    "--help": help,
    "-h": help,
    "initialize": initialize,
    "update_snps": update_snps,
    "update_publications": update_publications,
    "dump_publication": dump_publication,
    "dump_snp": dump_snp,
    "remove_duplicates_snps": remove_duplicates_snps
    }

if len(argv) == 2 and argv[1] in commands:
    commands[argv[1]]()
else:
    help()
