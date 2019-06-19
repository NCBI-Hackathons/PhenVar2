#!/usr/bin/env python3

import ncbiutils
from lxml import etree
import snp
import publication
import db
import time

"""
Finds all rsids that are explicitly cited in pubmed
and returns a list
"""
def get_complete_rsids():
    results = ncbiutils.esearch(db="snp", retmode="json", retmax=200000, retstart=0, term='snp_pubmed_cited[sb]', api_key="7c0213f7c513fa71fe2cb65b4dfefa76fb09")
    rsidlist = results["esearchresult"]["idlist"]
    return(rsidlist)

"""
Generates a list of PMIDs that are explicitly cite a given rsid
"""
def get_pmids(rsid):
    searchterm = "rs" + rsid + "+AND+pubmed_snp_cited[sb]"
    results = ncbiutils.esearch(db="pubmed", retmode="json", retmax=200000, restart=0, term=searchterm, api_key="7c0213f7c513fa71fe2cb65b4dfefa76fb09")
    pmidlist = results["esearchresult"]["idlist"]
    return(pmidlist)


"""
Takes a pmid and returns the abstract text
"""
def get_publication(pmid):
    raw = ncbiutils.efetch(db="pubmed", id=pmid, rettype="abstract", api_key="7c0213f7c513fa71fe2cb65b4dfefa76fb09")
    raw = raw.replace("<i>", "")
    raw = raw.replace("</i>", "")
    raw = raw.replace("<b>", "")
    raw = raw.replace("</b>", "")
    raw = raw.replace("<u>", "")
    raw = raw.replace("</u>", "")
    xml = etree.fromstring(raw)
    abstracts = []
    for a in xml.xpath('//AbstractText'):
        abstracts.append(a.text)
    titles = []
    for t in xml.xpath('//ArticleTitle'):
        titles.append(t.text)
    if len(titles) > 0 and titles[0] != None:
        titles = " ".join(titles)
    else:
        titles = ""
    if len(abstracts) > 0 and abstracts[0] != None:
        abstracts = " ".join(abstracts)
    else:
        abstracts = ""
    items = { "title": titles, "abstract": abstracts, }
    return(items)

"""
Initializes Snp objects and creates a list of them.  This list
can be later used to initilize a database or other magic
"""
def init_rsids():
    snps = []
    rsids = get_complete_rsids()
    for rsid in rsids:
        pmids = get_pmids(rsid)
        if len(pmids) > 0:
            a_snp = snp.Snp(id=rsid, publications=pmids)
            snps.append(a_snp)
    return(snps)
        
def init_pubs(snps):
    return()

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
                if not db.check_snp(conn=conn, id=s, pub=p):
                    db.add_snp(conn, s, p)
                if not db.check_publication(conn=conn, id=p):
                    info = get_publication(p)
                    db.add_publication(conn, id=p, title=info["title"], abstract=info["abstract"])
                p_pubs = p_pubs + 1
                print("Procssed {} pubs".format(p_pubs))
    return()

def main():
    conn = db.connect("db.sqlite3")
    db.create_tables(conn)
    init_db(conn)
    db.close(conn)
    return()

if __name__ == '__main__':
    main()

