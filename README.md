# PhenVar
PhenVar (now at 2.0!) is designed to take one or more rsids and generate a list of PubMed IDs to query and generate novel associations between publications. It utilizes a local database to store explicitly cited rsids and their associated publications to increase speed.  

## Version 2.0 Changes
PhenVar 2.0 is inteded to be a complete rewrite.  The old version was unmaintainable, as the database update functions were broken and reliant on old methods for accessing data from NCBI.  The new version is intended to fix these issues, but also introduces an API to make the data programmatically accessible.  The frontend will remain largely the same in terms of functionality, but will rely on the API for retrieiving data from the backend.  

Over time, as development continues, the API will be parameterized to allow better filtering of results through custom filter lists, limitations on depth of networks generated, etc.  

## Docker Container (coming soon!)
We will be creating a Docker container for distribution so that groups who are trying to use PhenVar at scale to extend other projects, at least during development, will have a local instance of the database (SQLite, ready-to-go in the container!).  During the container build process the database will be populated from our copy.  Once built and running, the local API can be used just like our remote API but without the network overhead and rate-limiting!  

## Updated ncbiutils.py
Biopython is a big import, and Entrez takes time!  We wrote our own ncbiutils, to be released as its own package later, for querying and interacting with NCBI resources via their HTTP API.  It's fast, extensible, and easy!
