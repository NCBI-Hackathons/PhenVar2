#!/usr/bin/env python3

import ncbiutils
from lxml import etree
import snp
import publication
import db2
import time

"""
Finds all rsids that are explicitly cited in pubmed
and returns a list
"""
def get_complete_rsids():
    results = ncbiutils.esearch(db="snp", retmode="json", retmax=200, retstart=0, term='snp_pubmed_cited[sb]', api_key="7c0213f7c513fa71fe2cb65b4dfefa76fb09")
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


def main():
    engine, session = db2.create("sqlite:///db.sqlite3")
    db2.create_tables(engine)
    init_db(session)
    return()

if __name__ == '__main__':
    main()
