import db2
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


def init_db(conn):
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
                db2.add_snp(conn, s, p)
                if not db2.check_publication(session=conn, id=p):
                    info = get_publication(p)
                    db2.add_publication(conn, id=p, title=info["title"], abstract=info["abstract"])
                p_pubs = p_pubs + 1
                print("Procssed {} pubs".format(p_pubs))
    return()


def initialize():
    engine, session = db2.create("sqlite:///db.sqlite3")
    db2.create_tables(engine)
    init_db(session)
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
