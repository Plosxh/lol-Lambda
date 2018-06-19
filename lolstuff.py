import json
import requests
import json
import os
import urllib.parse
from elasticsearch import Elasticsearch, RequestsHttpConnection, TransportError
from elasticsearch import RequestError
# from aws_requests_auth.aws_auth import AWSRequestsAuth

INDEX_MAPPING = {
    "mappings": {
        "doc": {
            "properties": {
                "id": {"type": "keyword"},
                "accountId": {"type": "keyword"},
                "name": {"type": "keyword"},
                "profileIconId": {"type": "keyword"},
                "revisionDate": {"type": "keyword"},
                "summonerLevel": {"type": "keyword"}
            }
        }
    }
}

def main():
    conf =""
    with open('conf.json') as f:
        conf = json.load(f)
    summonerID = getSummoner(conf["summonerName"])
    print(summonerID)
    es_client = Elasticsearch(
                    host="localhost",
                    port=9200,
                )
    create_index(es_client,conf["elasticsearch"]["index"])
    es_client.index(index=conf["elasticsearch"]["index"],
                    doc_type=conf["elasticsearch"]["type"],
                    body=summonerID,
                    id=summonerID["id"])

def create_index(es_client, index):
    """
        Create the ElasticSearch Index if it doesn't exist
    """
    try:
        res = es_client.indices.exists(index)
        if res is False:
            es_client.indices.create(index, body=INDEX_MAPPING)
            return 1
    except (ConnectionError, ConnectionRefusedError, RequestError):
        logger.info("Check ElasticSearch instances, must not be viable or healthy")



def getMatchs(summonerID):
    reconstructUrl =conf["lol"]["baseURL"]+conf["lol"]["matchListURL"]+str(summonerID)+"?api_key="+conf["lol"]["apiKey"]

def getSummoner(summoner,conf):
    summoner.replace(" ", "%20")
    reconstructUrl =conf["lol"]["baseURL"]+conf["lol"]["summonerURL"]+conf["lol"]["summonerName"]+conf["lol"]["apiKey"]
    print(reconstructUrl)
    req = requests.get(reconstructUrl)
    # print(req.content)
    account = json.loads(req.content)
    return account

if __name__ == '__main__':
    main()
