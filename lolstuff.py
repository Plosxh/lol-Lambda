import json
import requests
import json
import os
import urllib.parse
from elasticsearch import Elasticsearch, RequestsHttpConnection, TransportError
from elasticsearch import RequestError
# from aws_requests_auth.aws_auth import AWSRequestsAuth
slack_data = {}

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
    allSummonerIDs  =[]
    with open('conf.json') as f:
        conf = json.load(f)
    for invocateur in conf["lol"]["summonerName"]:
        summonerID = getSummoner(invocateur,conf)
        print(summonerID)
        allSummonerIDs.append(summonerID)
    for summ in allSummonerIDs:
        myMatchs=getMatchs(summ["accountId"],conf)
        for match in myMatchs["matches"]:
            participants = ""
            selectedMatch = getMatchInfos(match["gameId"],conf)
            for player in selectedMatch["participantIdentities"]:
                print(player)
                participants += player["player"]["summonerName"] +", "
            print(selectedMatch["teams"])
            slack_data['text']="you played with: "+participants
            resp = requests.post(conf["slack"]["webhookURL"], data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
            break
    # es_client = Elasticsearch(
    #                 host="localhost",
    #                 port=9200,
    #             )
    # create_index(es_client,conf["elasticsearch"]["index"])
    # es_client.index(index=conf["elasticsearch"]["index"],
    #                 doc_type=conf["elasticsearch"]["type"],
    #                 body=summonerID,
    #                 id=summonerID["id"])

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


def getMatchInfos(matchID,conf):
    reconstructUrl ="https://"+conf["lol"]["server"]+conf["lol"]["baseURL"]+conf["lol"]["matchURL"]+str(matchID)+"?api_key="+conf["lol"]["apiKey"]
    req = requests.get(reconstructUrl)
    match = json.loads(req.content)
    return match

def getMatchs(summonerID,conf):
    reconstructUrl ="https://"+conf["lol"]["server"]+conf["lol"]["baseURL"]+conf["lol"]["matchListURL"]+str(summonerID)+"?api_key="+conf["lol"]["apiKey"]
    req = requests.get(reconstructUrl)
    matchList = json.loads(req.content)
    return matchList

def getSummoner(invocateur,conf):
    summoner=invocateur.replace(" ", "%20")
    print("pouet")
    reconstructUrl ="https://"+conf["lol"]["server"]+conf["lol"]["baseURL"]+conf["lol"]["summonerURL"]+summoner+"?api_key="+conf["lol"]["apiKey"]
    # reconstructUrl = "toto"
    print(reconstructUrl)
    req = requests.get(reconstructUrl)
    # print(req.content)
    account = json.loads(req.content)
    return account

if __name__ == '__main__':
    main()
