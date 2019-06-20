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
                db.add_snp(session, s, p)
                if not db.check_publication(session=session, id=p):
                    info = get_publication(p)
                    db.add_publication(session, id=p, title=info["title"], abstract=info["abstract"])
                p_pubs = p_pubs + 1
                print("Procssed {} pubs".format(p_pubs))
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
