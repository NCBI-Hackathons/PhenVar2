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

parser = reqparse.RequestParser()
# parser.add_argument('Snp')

engine, session = db.create("sqlite:///db.sqlite3")

class Publication(Resource):
    def get(self, pmid):
        abort_if_no_pub(pmid)
        return jsonify(session.query(db.Publication).filter_by(pmid=pmid).scalar().as_dict())

class Snp(Resource):
    def get(self, rsid):
        abort_if_no_snp(rsid)
        return jsonify(session.query(db.Snp).filter_by(rsid=rsid).scalar().as_dict())


def abort_if_no_pub(pmid):
    if session.query(db.Publication).filter_by(pmid=pmid).scalar() == None:
        abort(404, message="Publication pm{} not found".format(pmid))

def abort_if_no_snp(rsid):
    if session.query(db.Snp).filter_by(rsid=rsid).scalar() == None:
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

api.add_resource(Snp, '/snps/<rsid>')

if __name__ == '__main__':
    app.run(debug=True)
