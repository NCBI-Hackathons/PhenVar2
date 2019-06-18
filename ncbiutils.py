#!/usr/bin/env python3

import requests

"""
Used to make an esearch and get the results back in json
"""
def esearch(**kwargs):
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
    args = []
    for key, value in kwargs.items():
        args.append(key+"="+str(value))
    qstring = "&".join(args)
    resp = requests.get(BASE_URL + qstring)
    if resp.status_code == 200:
        results = resp.json()
        return(results)
    else:
        print("You've encountered an error and we can't return your results")

"""
Used for an efetch, which is primarily to query specific IDs in dbsnp or pubmed
Doesn't return json, but must return XML, apparently.  
"""
def efetch(**kwargs):
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    args = []
    for key, value in kwargs.items():
        args.append(key+"="+str(value))
    qstring = "&".join(args)
    resp = requests.get(BASE_URL + qstring)
    if resp.status_code == 200:
        results = resp.text
        return(results)
    else:
        print("You've encountered an error and we can't return your results")