#!/usr/bin/env python3

import ncbiutils
from lxml import etree
import snp
import publication
import db

"""
Finds all rsids that are explicitly cited in pubmed
and returns a list
"""
def get_complete_rsids():
    results = ncbiutils.esearch(db="snp", retmode="json", retmax=500, retstart=0, term='snp_pubmed_cited[sb]', api_key="7c0213f7c513fa71fe2cb65b4dfefa76fb09")
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
def get_abstract(pmid):
    raw = ncbiutils.efetch(db="pubmed", id=pmid, rettype="abstract", api_key="7c0213f7c513fa71fe2cb65b4dfefa76fb09")
    xml = etree.fromstring(raw)
    abstracts = []
    for a in xml.xpath('//AbstractText'):
        abstracts.append(a.text)
    titles = []
    for t in xml.xpath('//ArticleTitle'):
        titles.append(t.text)
    print(titles)
    return()

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
        print(len(snps))
    return(snps)
        
def init_pubs(snps):
    return()

def main():
    snps = init_rsids()
    conn = db.connect("db.sqlite3")
    db.create_tables(conn)
    for item in snps:
        for pub in item.publications:
            db.add_snp(conn, item.id, pub)
    db.close(conn)
    return()

if __name__ == '__main__':
    main()
