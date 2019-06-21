#!/usr/bin/env python3

import ncbiutils
from lxml import etree
import db
import time
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort
import json

app = Flask(__name__)
api = Api(app)

# Arg parsing mostly for multiple args/a POST request.
# parser = reqparse.RequestParser()
# parser.add_argument('Snp')

engine, session = db.create("sqlite:///db.sqlite3")

class Publication(Resource):
    def get(self, pmid):
        abort_if_no_pub(pmid)
        # snps = session.query(db.Snp).filter_by(publications=pmid)
        # pubs = session.query(db.Publication).filter_by(rsids=pmid)
        return jsonify(session.query(db.Publication).filter_by(rsids=pmid).scalar().as_dict())

class Snp(Resource):
    def get(self, rsid):
        abort_if_no_snp(rsid)
        snps = session.query(db.Snp).filter_by(rsid=rsid)
        pubs = session.query(db.Publication).filter_by(rsids=snps.first().publications)
        # Publications that registered the SNP
        pubs_dict = {int(pub.id): pub.as_dict() for pub in pubs}
        # Add SNP objects that each publication registered
        for pub in pubs_dict.items():
            pub[1]['snps'] = {snp.rsid: snp.as_dict() for snp in session.query(db.Snp).filter_by(publications=pub[1]['rsids'])}
        return jsonify({'publications': pubs_dict})


def abort_if_no_pub(pmid):
    if session.query(db.Publication).filter_by(rsids=pmid).first() == None:
        abort(404, message="Publication {} not found".format(pmid))

def abort_if_no_snp(rsid):
    if session.query(db.Snp).filter_by(rsid=rsid).first() == None:
        abort(404, message="SNP rs{} not found".format(rsid))

"""
Finds all rsids that are explicitly cited in pubmed
and returns a list
"""
def get_complete_rsids():
    results = ncbiutils.esearch(db="snp", retmode="json", retmax=1000, retstart=0, term='snp_pubmed_cited[sb]', api_key="7c0213f7c513fa71fe2cb65b4dfefa76fb09")
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
    if len(titles) > 0 and not None in titles:
        titles = " ".join(titles)
    else:
        titles = ""
    if len(abstracts) > 0 and not None in abstracts:
        abstracts = " ".join(abstracts)
    else:
        abstracts = ""
    items = { "title": titles, "abstract": abstracts, }
    return(items)

api.add_resource(Snp, '/api/v1/snp/<rsid>')
api.add_resource(Publication, '/api/v1/pub/<pmid>')

if __name__ == '__main__':
    app.run(debug=True)
