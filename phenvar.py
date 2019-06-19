#!/usr/bin/env python3

import ncbiutils
from lxml import etree
import snp
import publication

"""
Finds all rsids that are explicitly cited in pubmed
and returns a list
"""
def get_complete_rsids():
    results = ncbiutils.esearch(db="snp", retmode="json", retmax=200000, retstart=0, term='snp_pubmed_cited[sb]', api_key="7c0213f7c513fa71fe2cb65b4dfefa76fb09")
    rsidlist = results["esearchresult"]["idlist"]
    for x in range(0, len(rsidlist)):
        rsidlist[x] = "rs" + rsidlist[x]
    return(rsidlist)

"""
Generates a list of PMIDs that are explicitly cite a given rsid
"""
def get_pmids(rsid):
    searchterm = rsid + "+AND+pubmed_snp_cited[sb]"
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
        
def main():
    snps = init_rsids()
    return()

if __name__ == '__main__':
    main()
