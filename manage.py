#!/usr/bin/env python3
import db
from phenvar import get_complete_rsids, get_pmids, get_publication
import time
from sys import argv


help_text = """USAGE:
./manage.py <command>
 commands:
    - initialize    creates tables in database, should only be run once
"""


def help():
    print(help_text)

def initialize():
    engine, session = db.create("sqlite:///db.sqlite3")
    db.create_tables(engine)
    update_snps(session)
    update_publications(session)
    db.close(session)

def update_snps(session):
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
                    print("snp not in database; adding")

    return()

def update_publications(session):
    p_pubs = 0
    # for row in snps_publications get pmid
    rows = db.get_snp_rows(session)
    for row in rows:
        pmid = row.publications
        # check if pmid in db, add if not
        if not db.check_publication(session=session, id=pmid):
            info = get_publication(pmid)
            db.add_publication(session, id=pmid, title=info["title"], abstract=info["abstract"])
            print("publication not in database; adding")
        p_pubs += 1
        print("Processed {} pubs".format(p_pubs))
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
}

if len(argv) == 2 and argv[1] in commands:
    commands[argv[1]]()
else:
    help()
